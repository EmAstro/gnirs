import argparse
import numpy as np
# from IPython import embed

from gnirs.photometry import photometry
from gnirs import __version__

EXAMPLES = str(r"""EXAMPLES:""" + """\n""" + """\n""" +
               r""">>> fit_arc2d --data_directory ./Data/ --pivot_fw1_filter """ + """\n""" +
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
    from gnirsarc2d.io import read_iraf_database
    if type(args.database_directory) == list:
        database_directory = args.database_directory[0]
    else:
        database_directory = args.database_directory
    if type(args.root_filename) == list:
        root_filename = args.root_filename[0]
    else:
        root_filename = args.root_filename
    if type(args.configuration) == list:
        configuration = gnirs.GnirsConfiguration(name=args.configuration[0])
    else:
        configuration = gnirs.GnirsConfiguration(name=args.configuration)
    if type(args.fit_function) == list:
        fit_function = args.fit_function[0]
    else:
        fit_function = args.fit_function
    if type(args.fit_order_spec) == list:
        fit_order_spec = args.fit_order_spec[0]
    else:
        fit_order_spec = args.fit_order_spec
    if type(args.fit_order_order) == list:
        fit_order_order = args.fit_order_order[0]
    else:
        fit_order_order = args.fit_order_order

    pixel, wavelength_iraf, wavelength_archive, order = [], [], [], []
    for slit in configuration.order["slit"]:
        pixel_slit, wavelength_iraf_slit, wavelength_archive_slit = read_iraf_database.get_features_from_identify_table(
            database_directory + root_filename + "_" + str(slit) + "_")
        order_number = configuration.order['number'][configuration.order['slit'].index(int(slit))]
        order_slit = [order_number] * len(pixel_slit)
        pixel.extend(pixel_slit)
        wavelength_iraf.extend(wavelength_iraf_slit)
        wavelength_archive.extend(wavelength_archive_slit)
        order.extend(order_slit)
    fit2d, mask = arc2d.full_fit(np.array(pixel), np.array(wavelength_archive), np.array(order),
                                 tot_pixel=configuration.cols, fit_function=fit_function,
                                 fit_order_spec=fit_order_spec, fit_order_order=fit_order_order)
    arc2d.plot_fit(fit2d, mask, np.array(pixel), np.array(wavelength_archive), np.array(order),
                   tot_pixel=configuration.cols)

    return
