import numpy as np
import unittest
import logging
import json
import time
import os

from collections import OrderedDict
from error_correction import codes


decoder_names = ['ML', 'SPA', 'MSA', 'LP', 'ADMM', 'ADMMA']

strl = lambda ll: (str(it_) for it_ in ll)






def setup_console_logger(level=logging.DEBUG):
    logging.basicConfig(format='%(name)s|%(message)s', level=level)


def setup_file_logger(path, name, level=logging.DEBUG):
    logging.basicConfig(filename=os.path.join(path, '%s.log' % name),
                        filemode='a',
                        format='%(asctime)s,%(msecs)03d|%(name)s|%(levelname)s|%(message)s',
                        datefmt='%H:%M:%S',
                        level=level)
    logging.info('Logger init to file. %s' % ('%' * 80))




class Saver:
    def __init__(self, data_dir, run_ids):
        self.dict = OrderedDict(run_ids)
        make_dir_if_not_exists(data_dir)
        dir_path, file_name = data_dir, '-'.join(strl(self.dict.values()))
        self.file_path = os.path.join(dir_path, '%s.json' % file_name)

    def add_meta(self, key, val):
        self.dict[key] = val

    def add(self, param, val_dict):
        data = load_json(self.file_path)
        if data is None:
            data = OrderedDict()
            for key in self.dict: data[key] = self.dict[key]
            for key in val_dict: data[key] = {}

        for key in val_dict: data[key][str(param)] = val_dict[key]
        self.write_(data)

    def write_(self, data):
        with open(self.file_path, 'w') as fp:
            json.dump(data, fp, indent=4)

    def add_all(self, val_dict):
        z = self.dict.copy()
        z.update(val_dict)
        self.write_(z)

    def add_deprecated(self, run_id, val):
        data = self.load({})
        temp = data
        for key in run_id[0:-1]:
            if key not in temp.keys(): temp[key] = {}
            temp = temp[key]
        temp[run_id[-1]] = val

        with open(self.file_path, 'w') as ff:
            json.dump(data, ff)

import signal
import time

class DelayedInterrupt:
    """ Context manager that delays handling SIGINT until after a safe section. """
    
    stop_signal = False  # Class variable to store the signal state

    def __init__(self, logger):
        self.original_handler = None
        self.interrupted = False  # Instance variable to track local interruptions
        self.logger = logger

    def signal_handler(self, sig, frame):
        """ Capture the interrupt signal but delay handling until after the block. """
        self.logger.warning("\nSignal received! Waiting for the critical section to finish...")
        DelayedInterrupt.stop_signal = True  # Mark signal for handling later

    def __enter__(self):
        """ Set up the signal handler. """
        self.original_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self.signal_handler)
        return self  # The instance itself is returned

    def __exit__(self, exc_type, exc_value, traceback):
        """ Restore the original signal handler on exit. """
        signal.signal(signal.SIGINT, self.original_handler)

        DelayedInterrupt.stop_signal = False 

class LoopProfiler:
    class Tag:
        def __init__(self, name, line, prof):
            self.name, self.line, self.prof = name, line, prof

        def elapsed(self):
            return (time.time() - self.updated) * 1000

        def __enter__(self):
            self.updated = time.time()
            extra = '' if self.line is None else ': ' + self.line
            self.prof.log.debug("(( '" + self.name + "'" + extra)
            return self

        def __exit__(self, type, value, traceback):
            elapsed = self.elapsed()
            self.prof.log.debug('    elapsed[%s] ))' % str(int(elapsed)))
            self.prof.tags[self.name] = self.prof.tags.get(self.name, 0) + elapsed

    def __init__(self, log, dump_freq):
        self.log = log
        self.updated = time.time()
        self.dump_freq = dump_freq
        self.tags = OrderedDict()
        self.step_count = 0

    def __enter__(self):
        return self

    def start(self, line=None):
        self.step_count += 1
        if line is not None: self.log.debug(line)
        return self

    def tag(self, name, line=None):
        return LoopProfiler.Tag(name, line, self)

    def __exit__(self, typ, value, traceback):
        if self.dump_freq > 0 and self.step_count % self.dump_freq == 0:
            summary = ', '.join(["'%s':%d" % (key, int(val)) for key, val in self.tags.items()])
            self.log.info('Summary at[%d] for[%d]: [' % (self.step_count, self.dump_freq) + summary + ']')
            for key in self.tags: self.tags[key] = 0
