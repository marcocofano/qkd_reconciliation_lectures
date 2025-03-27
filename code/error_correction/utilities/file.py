from itertools import zip_longest
import csv
import os
import re


def resolve_data_dir(proj_name):
    scratch = os.path.join(os.path.expanduser('~'), 'scratch')
    return os.path.join(scratch, proj_name)

def resolve_data_dir_os(proj_name, extra=[]):
    if os.name == 'nt': # if windows
        curr_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(curr_path, '..', '..', 'data', *extra)
    else:
        return resolve_data_dir(proj_name)


class CSVFile:
    def __init__(self, file_name, work_dir=None, header=None, mode='w'):
        path = file_name if work_dir is None else os.path.join(work_dir, file_name)
        self.fp = open(path, mode, newline='')
        self.csv = csv.writer(self.fp, delimiter=',')
        if header is not None: self.csv.writerow(header)
        self.header = header

    def writerow(self, line, flush=False):
        self.csv.writerow(line)
        if flush: self.flush()

    def flush(self): self.fp.flush()

    def __del__(self):
        self.fp.flush()
        self.fp.close()


def gen_unique_labels(long_names, tokens=['_', '__']):
    def inner(strings, token):
        spls = [ss.split(token) for ss in strings]
        sets = [set(spl) for spl in spls]
        common = set().union(*sets)
        common.intersection_update(*sets)
        return ['_'.join(it for it in spl if it not in common) for spl in spls]

    if len(long_names)>1:
        for tk in tokens: long_names = inner(long_names, tk)
        return long_names
    else:
        return ['plot']

def filter_strings(_a, dirs):
    kw_filter = lambda nl_,f_,kwl: [n_ for n_ in nl_ if f_(kw in n_ for kw in kwl)]
    if _a.not_kw: dirs = [dir for dir in dirs if all(kw not in dir for kw in _a.not_kw)]
    if _a.and_kw: dirs = kw_filter(dirs, all, _a.and_kw)
    if _a.or_kw: dirs = kw_filter(dirs, any, _a.or_kw)
    if not dirs: print(f'No matches for', 'NOT:', _a.not_kw, ', AND:', _a.and_kw, ', OR:', _a.or_kw)
    else: print('Collected:', *dirs, sep='\n')
    return dirs

def filter_directories(_a, data_dir):
    dirs = filter_strings(_a, next(os.walk(data_dir))[1])
    if not dirs: print(f'No matching directories found in {data_dir}.')
    else: print('Collected %d directories.'%len(dirs))
    return dirs

# https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
def naturalkey(text):
    atoi = lambda tt: int(tt) if tt.isdigit() else tt
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def reorder(_a, dir_labels):
    strings = [f'{dir} >> [{lab}]' for dir,lab in dir_labels]
    ord = _a.order
    if ord:
        ord = [o_ for o_,_ in zip_longest(ord, dir_labels, fillvalue=-1)]
        strings = [f'[{o_:g}] {old}' for o_,old in zip(ord, strings)]
        dir_labels.sort(key=dict(zip(dir_labels, ord)).get)
    elif _a.natsort:
        dir_labels.sort(key=lambda it: naturalkey(it[1]))

    print(*strings, sep='\n')
    if _a.reverse: dir_labels.reverse()

def bind_filter_args(parser):
    parser.add_argument('--and_kw', help='AND filter: allows only if all present', default=[], type=str, nargs='*')
    parser.add_argument('--or_kw', help='OR filter: allows if any is present', default=[], type=str, nargs='*')
    parser.add_argument('--not_kw', help='NOT filter: allows only if these are NOT present', default=[], type=str, nargs='*')

def bind_reorder_args(parser):
    parser.add_argument('--order', help='re-order dir list, biggest at the front', type=float, nargs='+')
    parser.add_argument('--natsort', help='sort by natural order of labels', action='store_true')
    parser.add_argument('--reverse', help='reverse after sorting', action='store_true')
