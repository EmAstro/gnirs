import numpy as np
from pathlib import Path
from astropy.io import fits


class GnirsFits:
    def __init__(self):
        self._fits_file = None
        self._hdul = None
        self._data_type = None
        self._pixel_scale = None
        self._filter_one = None
        self._filter_two = None

    @property
    def fits_file(self):
        return self._fits_file

    @fits_file.setter
    def fits_file(self, fits_file):
        if Path(fits_file).is_file():
            self._fits_file = fits_file
            self._hdul = fits.open(fits_file)
        else:
            raise ValueError('File {} not found'.format(fits_file))

    @property
    def data_type(self):
        return self._data_type

    # ToDo Add the option to read it from the header and, if set by the user, to check in the header if this
    #      is consistent.
    @data_type.setter
    def data_type(self, data_type):
        self._data_type = data_type

    @property
    def pixel_scale(self):
        return self._pixel_scale

    # ToDo Add the option to read it from the header and, if set by the user, to check in the header if this
    #      is consistent.
    # ToDo In case units are not present, it should be added with a warning.
    @pixel_scale.setter
    def pixel_scale(self, pixel_scale):
        self._pixel_scale = pixel_scale

    @property
    def primary_header(self):
        return self._hdul[0].header

    @primary_header.setter
    def primary_header(self, primary_header):
        self._hdul[0].header = primary_header

    @property
    def filter_one(self):
        return self._filter_one

    @filter_one.setter
    def filter_one(self, filter_one):
        self._filter_one = filter_one

    @property
    def filter_two(self):
        return self._filter_two

    @filter_two.setter
    def filter_two(self, filter_two):
        self._filter_two = filter_two






