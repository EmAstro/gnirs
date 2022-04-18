import numpy as np
from pathlib import Path
from astropy.io import fits


class GnirsFits:
    def __init__(self, fits_file, data_type=None, pixel_scale=None, filter_one=None, filter_two=None):
        self.fits_file = fits_file
        self.data_type = data_type
        self.pixel_scale = pixel_scale
        self.filter_one = filter_one
        self.filter_two = filter_two

    @property
    def fits_file(self):
        return self.__fits_file

    @fits_file.setter
    def fits_file(self, fits_file):
        if Path(fits_file).is_file():
            self.__fits_file = fits_file
            self.hdul = fits.open(fits_file)
        else:
            raise ValueError('File {} not found'.format(fits_file))

    @property
    def data_type(self):
        return self.__data_type

    # ToDo Add the option to read it from the header and, if set by the user, to check in the header if this
    #      is consistent.
    @data_type.setter
    def data_type(self, data_type):
        self.__data_type = data_type

    @property
    def pixel_scale(self):
        return self.__pixel_scale

    # ToDo Add the option to read it from the header and, if set by the user, to check in the header if this
    #      is consistent.
    # ToDo In case units are not present, it should be added with a warning.
    @pixel_scale.setter
    def pixel_scale(self, pixel_scale):
        self.__pixel_scale = pixel_scale

    @property
    def filter_one(self):
        return self.__filter_one

    @filter_one.setter
    def filter_one(self, filter_one):
        self.__filter_one = filter_one

    @property
    def filter_two(self):
        return self.__filter_two

    @filter_two.setter
    def filter_two(self, filter_two):
        self.__filter_two = filter_two

    @property
    def hdul(self):
        return self.__hdul

    @hdul.setter
    def hdul(self, hdul):
        self.__hdul = hdul

    def get_data(self):
        return self.hdul[1].data




