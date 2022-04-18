"""
This module performs some quick photometry on gnirs imaging data

Attributes:
    CENTROID_FUNCTIONS (list): list of the implemented functions used to estimate the centroid. The full description
        of them is in the `photutils centroids manual`_.

.. _photutils centroids guide:
   https://photutils.readthedocs.io/en/stable/centroids.html
"""


from astropy import units as u

from photutils.centroids import centroid_com, centroid_quadratic
from photutils.centroids import centroid_1dg, centroid_2dg
from photutils.centroids import centroid_sources

from photutils.aperture import CircularAnnulus
from photutils.aperture import ApertureStats

from gnirs.utils import types


CENTROID_FUNCTIONS = [None, 'com', 'quadratic', '1dg', '2dg']




def _make_annular_aperture(location, radius_in, radius_out):
    """Given a starting point and two radii returns a annular aperture object

    Args:
        location (tuple): location (x,y) with x and y as :obj:`astropy.quantity`
        radius_in (:obj:`astropy.quantity`): inner radius in pixels
        radius_out (:obj:`astropy.quantity`): outer radius in pixels

    Returns:
        :obj:`photutils.aperture`: Annular aperture

    """
    if radius_in is not None and radius_out is not None:
        annular_aperture = CircularAnnulus(location, r_in=radius_in, r_out=radius_out)
    else:
        annular_aperture = None
    return annular_aperture


def _get_preferred_location(initial_location, refined_location):
    """Returns refined location if defined otherwise return the initial location

    Args:
        initial_location (tuple): initial location (x,y)
        refined_location (tuple): refined location (x,y)

    Returns:
        tuple: if `refined_location` is set to None this is the `initial_location`, otherwise the `refined_location`

    """
    if refined_location is not None:
        return refined_location
    else:
        return initial_location

def _distance_in_pixels(location_1, location_2):
    distance_in_pixels = ((location_1[0]-location_2[0])**2. + (location_1[1]-location_2[1])**2.)**0.5
    return distance_in_pixels

def aperture_stats(data, aperture):
    if aperture is None:
        return None
    else:
        aperture_stats_result = ApertureStats(data, aperture)
    return aperture_stats_result.sum, aperture_stats_result.mean, aperture_stats_result.median, \
           aperture_stats_result.std

class CircularAperturePhotometry:
    """Class to run aperture photometry over a source

    Attributes:
        data (:obj:`numpy.ndarray`): image data
        initial_location (tuple): (x,y) location in pixel of the source on the image
        radius (float): radius from within which to calculate the photometry
        radius_bkg_in (float, optional): inner radius of the annulus where to calculate the background
        radius_bkg_out (float, optional): outer radius of the annulus where to calculate the background
        inverse_variance (:obj:`numpy.ndarray`, optional): inverse variance (i.e., sigma^-2) of the image
        centroid_function (str, optional): function used to determine the centroid

        data
        initial_location
        radius
        radius_bkg_in
        radius_bkg_out

    """

    def __init__(self, data, initial_location, radius, radius_bkg_in=None, radius_bkg_out=None, inverse_variance=None,
                 centroid_function=None):
        self.data = data
        self.initial_location = initial_location
        self.refined_location = None
        self.radius = radius
        self.aperture = None
        self.radius_bkg_in = radius_bkg_in
        self.radius_bkg_out = radius_bkg_out
        self.aperture_bkg = None

        self.centroid_function = centroid_function

        self.background = None
        self.inverse_variance = inverse_variance

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def initial_location(self):
        return self.__initial_location

    @initial_location.setter
    def initial_location(self, initial_location):
        if type(initial_location) is tuple:
            self.__initial_location = types.int_to_float(initial_location[0]), types.int_to_float(initial_location[1])
        else:
            raise TypeError(r"initial_location needs to be of type tuple")

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, radius):
        self.__radius = types.int_to_float(radius)

    @property
    def radius_bkg_in(self):
        return self.__radius_bkg_in

    @radius_bkg_in.setter
    def radius_bkg_in(self, radius_bkg_in):
        self.__radius_bkg_in = types.int_to_float(radius_bkg_in)
        try:
            self.aperture_bkg = _make_annular_aperture(_get_preferred_location(self.initial_location,
                                                                               self.refined_location),
                                                       self.radius_bkg_in, self.radius_bkg_out)
        except AttributeError:
            pass


    @property
    def radius_bkg_out(self):
        return self.__radius_bkg_out

    @radius_bkg_out.setter
    def radius_bkg_out(self, radius_bkg_out):
        self.__radius_bkg_out = types.int_to_float(radius_bkg_out)
        try:
            self.aperture_bkg = _make_annular_aperture(_get_preferred_location(self.initial_location,
                                                                               self.refined_location),
                                                       self.radius_bkg_in, self.radius_bkg_out)
        except AttributeError:
            pass

    @property
    def refined_location(self):
        return self.__refined_location

    @refined_location.setter
    def refined_location(self, refined_location):
        if refined_location is None:
            self.__refined_location = None
        elif type(refined_location) is tuple:
            self.__refined_location = types.int_to_float(refined_location[0]), types.int_to_float(refined_location[1])
        else:
            raise TypeError(r"refined_location needs to be of type tuple")

    @property
    def centroid_function(self):
        return self.__centroid_fuction

    @centroid_function.setter
    def centroid_function(self, centroid_function):
        if centroid_function is None:
            self.__centroid_function = None
            self.refined_location = None
        elif centroid_function == 'com':
            self.__centroid_function = centroid_com
        elif centroid_function == 'quadratic':
            self.__centroid_function = centroid_quadratic
        elif centroid_function == '1dg':
            self.__centroid_function = centroid_1dg
        elif centroid_function == '2dg':
            self.__centroid_function = centroid_2dg
        else:
            raise ValueError(r'Centroid function not supported. Possibilities are: \n'
                             r'{}'.format(CENTROID_FUNCTIONS))
        if centroid_function is not None:
            # ToDo make them input
            condition_distance = 2.* self.radius
            while (condition_distance > 0.5) & (condition_distance <= 2.* self.radius):
                old_location = _get_preferred_location(self.initial_location, self.refined_location)
                old_refined_location = self.refined_location
                # The initial guess is first used to calculate the background
                _, average_bkg, median_bkg, std_bkg = self.background_stats()
                x_centroid, y_centroid =_get_preferred_location(self.initial_location,
                                                                self.refined_location)
                if median_bkg is None:
                    data_bkg_subtracted = self.data
                else:
                    data_bkg_subtracted = self.data - median_bkg
                self.refined_location = centroid_sources(data_bkg_subtracted,
                                                         x_centroid, y_centroid ,
                                                         box_size=int(2.*self.radius),
                                                         centroid_func=self.__centroid_function)
                # Update background aperture to new centroid
                self.aperture_bkg = _make_annular_aperture(_get_preferred_location(self.initial_location,
                                                                                   self.refined_location),
                                                           self.radius_bkg_in, self.radius_bkg_out)
                condition_distance = _distance_in_pixels(old_location, self.refined_location)
                if condition_distance > 2. * self.radius:
                    print("FAILED TO FIND CENTROID: you may need to try with a different radius")
                    self.refined_location = old_refined_location

            # sum_method='exact'

    def background_stats(self):
        if self.aperture_bkg is None:
            return None, None, None, None
        else:
            sum_bkg, mean_bkg, median_bkg, std_bkg = aperture_stats(self.data, self.aperture_bkg)
            return sum_bkg, mean_bkg, median_bkg, std_bkg

    def get_centroid(self):
        return _get_preferred_location(self.initial_location, self.refined_location)

