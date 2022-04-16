from gnirs.io import fits
from gnirs.photometry import photometry


def aperture_photometry(gnirs_fits, init_location, radius, radius_in_bkg, radius_out_bkg, refine_centroid=True,
                        centroid_function=None):
    if gnirs_fits.data_type != 'IMAGING':
        raise ValueError('data_type should be IMAGING and not {}'.format(gnirs_fits.data_type))

    return
