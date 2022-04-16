from astropy import units as u
from photutils.centroids import centroid_com, centroid_quadratic
from photutils.centroids import centroid_1dg, centroid_2dg

CENTROID_FUNCTIONS = [None, 'com', 'quadratic', '1dg', '2dg']






class Photometry:
    def __init__(self, data, init_location, radius, radius_in_bkg=None, radius_out_bkg=None, variance=None,
                 refine_centroid=False, centroid_function=None):
        self.data = data
        self.init_location = init_location
        self.radius = radius
        self.radius_in_bkg = radius_in_bkg
        self.radius_out_bkg = radius_out_bkg
        self.inv_variance = inv_variance
        self.refine_centroid = refine_centroid
        self.centroid_function = centroid_function
        self.refined_location = None

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def init_location(self):
        return self.__init_location

    @init_location.setter
    def init_location(self, init_location):
        if type(init_location) is tuple:
            init_x = init_location[0]
            init_y = init_location[1]
            if type(init_x) is int:
                init_x = float(init_x)

            self.__init_location = init_location
        else:
            raise TypeError(r'init_location needs to be of type tuple')
        return

    def refine_positions(self, centroid_function=None, update=True):
        if centroid_function not in CENTROID_FUNCTIONS:
            raise ValueError(r'Centroid function not supported. Possibilities are: \n'
                             r'{}'.format(CENTROID_FUNCTIONS))
        data = self.data
        x_centroids, y_centroids = 0., 0.
        return x_centroids, x_centroids
