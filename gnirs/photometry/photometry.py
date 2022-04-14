from photutils.centroids import centroid_com, centroid_quadratic
from photutils.centroids import centroid_1dg, centroid_2dg

CENTROID_FUNCTIONS = ['com', 'quadratic', '1dg', '2dg']


class Photometry:
    def __init__(self, data, positions, radii, inner_radii_bg, outer_radii_bg, variance=None):
        return

    def refine_positions(self, centroid_function='com', update=True):
        self.data
        x_centroids, y_centroids = 0., 0.
        return x_centroids, x_centroids


class PhotometrySingleObject(Photometry):
    def __init__(self):
        return
