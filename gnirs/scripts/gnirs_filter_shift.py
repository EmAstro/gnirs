import argparse
import numpy as np
# from IPython import embed

from gnirs.photometry import photometry
from gnirs import __version__

EXAMPLES = str(r"""EXAMPLES:""" + """\n""" + """\n""" +
               r""">>> gnirs_filter_shift --data_directory ./Data/ --pivot_fw1_filter """ + """\n""" +
               r""" """)


def parser(options=None):
    script_parser = argparse.ArgumentParser(
        description=r"""Fit of the wavelength solution for GNIRS data""" + """\n""" + """\n""" +
                    r"""The code looks for the lines identified with IRAF in the directory: `database_directory` """ +
                    r"""that is the format in which the GNIRS IRAF pipeline.""" + """\n""" +
                    """\n""" +
                    r"""This is version {:s}""".format(__version__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EXAMPLES)

    script_parser.add_argument("-d", "--data_directory", nargs="+", type=str, default="./Data/",
                               help=r"Path to the directory where the data are")
    script_parser.add_argument("-f1", "--pivot_fw1_filter", nargs="+", type=str, default=None,
                               help=r"Filter from wheel n. 1 respect to which the shifts from other filters are " +
                                    "calculated")
    script_parser.add_argument("-f2", "--pivot_fw2_filter", nargs="+", type=str, default=None,
                               help=r"Filter from wheel n. 2 respect to which the shifts from other filters are " +
                                    "calculated")
    if options is None:
        args = script_parser.parse_args()
    else:
        args = script_parser.parse_args(options)
    return args


def main(args):

    return
