import os
import logging
import argparse
from pathlib import Path

from error_correction.decoders import BPA, decoder_factory
from error_correction.channels import Channel, channel_factory

from error_correction.codes import Code, CodeConfig
from error_correction.performance import decoding_performance
from error_correction.data_dirs import ErrorCorrectionDirs

def get_code(name, data_dirs: ErrorCorrectionDirs):
    """Factory function to instantiate a code object from a slug"""
    config = CodeConfig.from_slug(name)
    return Code.from_config(config, data_dirs)


def setup_cli(logger):
    channel_names = ["bsc", "bec", "biawgn"]  #TODO: bec and biawgn not implemented yet
    decoder_names = ["spa", "msa"]
    codehelp = "Code for channel coding"
    # cwhelp = 'transmitted codeword [0:all-zero, 1:all-ones, -1:random from code book (works only with small codes)]'

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--channel", help="channel type", choices=channel_names, default="bsc"
    )
    parser.add_argument(
        "--code", help=codehelp, default="coo_1200_3-6-randldpc_1"
    )
    parser.add_argument(
        "--decoder", help="decoder type", choices=decoder_names, default="spa"
    )

    # parser.add_argument('--codeword', help=cwhelp, default=0, type=int, choices=[-1, 0, 1])
    parser.add_argument(
        "--min-fec",
        help="frame errors before aborting for the current parameter",
        default=100,
        type=int,
    )
    parser.add_argument(
        "--params",
        help="channel parameter, e.g. erasure probability for erasure channel",
        nargs="+",
        type=float,
        default=[0.1, 0.07, 0.06],
    )

    parser.add_argument(
        "--max-iter",
        help="max iteration count for iterative decoders",
        default=50,
        type=int,
    )
    parser.add_argument(
        "--data_dir",
        help="location for data directory",
        default=Path("data"),
    )

    parser.add_argument(
        "--log-freq", help="log frequency in seconds", default=5.0, type=float
    )
    return parser.parse_args()


def setup_console_logger(level=logging.DEBUG):
    logging.basicConfig(format="%(name)s|%(message)s", level=level)
    return logging.getLogger()


if __name__ == "__main__":
    logger = setup_console_logger(level=logging.INFO)
    args = setup_cli(logger)

    data_dirs = ErrorCorrectionDirs(root_path=args.data_dir)

    channel_class: Channel = channel_factory(args.channel)
    decoder_class: BPA = decoder_factory(args.decoder)
    logger.info(args.code)
    logger.info(data_dirs.codes)
    code = get_code(args.code, data_dirs)
    decoder = decoder_class(code.parity_mtx, max_iter=args.max_iter)

    decoding_performance(
        channel_class,
        decoder,
        code,
        args.params,
        data_dirs,
        args.min_fec,
        args.log_freq,
        logger,
    )
