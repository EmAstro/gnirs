from gnirs.io import fits
from gnirs.photometry import photometry


def get_centroid(gnirs_fits, initial_location, radius, radius_in_bkg, radius_out_bkg,
                 centroid_function='mod'):
    if gnirs_fits.data_type != 'IMAGING':
        raise ValueError('data_type should be IMAGING and not {}'.format(gnirs_fits.data_type))
    circular_aperture = photometry.CircularAperturePhotometry(gnirs_fits.get_data(), initial_location, radius,
                                                              radius_in_bkg, radius_out_bkg,
                                                              centroid_function=centroid_function)
    return circular_aperture.get_centroid()
