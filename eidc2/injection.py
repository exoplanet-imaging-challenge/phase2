#! /usr/bin/env python

"""
Module with routines used for the injection of fake companions in the context
of the Exoplanet Imaging Data Challenge
"""

__author__ = 'Valentin Christiaens'
__all__ = ['inject_fcp_ifs']

import numpy as np
from special.model_resampling import resample_model
from vip_hci.fm import cube_inject_companions


def inject_fcp_ifs(cube, derot_angles, psf, pos_rtheta, fcp_spec, star_spec, 
                   mean_contrast, spec_fwhm=None, transmission=None, 
                   imlib='vip-fft', interpolation=None, verbose=False):
    """ Function to inject a fake companion with a given input spectrum into an 
    IFS data cube.

    Parameters
    ----------
    cube : 4D numpy array
        IFS 4D master cube (temporal, spectral, y, x)
    derot_angles : 1D numpy array
        Array with derotation angles to align North up in the images. Should
        have same length as the first dimension of the 4D cube.
    psf: 3D numpy array
        3D array with the normalized point-spread function as a function of 
        wavelength (i.e. its first dimension should match the second dimension 
        of the 4D cube).
    pos_rtheta: tuple of 2 floats
        (r, theta) polar coordinates for the fake companion to be injected. 
        These coordinates are to be provided for the derotated image - although 
        the injection is performed in the yet non-derotated cube. Theta is the
        trigonometric angle counted from the positive x-axis.
    fcp_spec: 2D numpy array
        Spectrum to be injected. Dimensions should be (2 x n_channels),
        where the first dimension should provide the wavelengths in microns, 
        and the second the fluxes (arbitrary units). Does not necessarily have 
        to be resampled yet.
    star_spec: 2D numpy array
        Spectrum of the star, as measured by the IFU. Dimensions should be 
        (2 x n_channels), where the first dimension should provide the 
        wavelengths in microns, and the second the fluxes (arbitrary units).
    mean_contrast: float
        Requested mean contrast (over all channels) between the fake companion 
        and the star, used to scale the fluxes of the companion spectrum before
        injection.
    spec_fwhm: float, optional
        Spectral FWHM of the instrument in nm. If provided, it is used to 
        convolve the fcp spectrum before resampling to the IFU wavelength 
        sampling.
    transmission: numpy array, optional
        Radial transmission of the coronagraph, if any. Array with 2 columns.
        First column is the radial separation in pixels. Second column is the
        corresponding off-axis transmission (between 0 and 1).
    imlib : str, optional, {'vip-fft', 'opencv', 'ndimage-fourier'}
        Image library used for image shifts. See the documentation of the 
        ``vip_hci.preproc.frame_shift`` function.
    interpolation : str, optional
        Interpolation method used for image shifts. See the documentation of 
        the ``vip_hci.preproc.frame_shift`` function.
    verbose: str, optional
        Whether to print more information during processing.
    
    Returns
    -------
    fcp_cube : 4D numpy array
        Output IFS 4D master cube where the companion has been injected.

    """

    r, theta = pos_rtheta

    # convolve + resample the model spectrum
    res_spec = resample_model(star_spec[0], fcp_spec[0], fcp_spec[1],
                              instru_fwhm=spec_fwhm)
    
    # find flux scaling factor
    scal_fac = mean_contrast*np.sum(star_spec[1])/np.sum(res_spec[1])
    flevel = scal_fac*res_spec[1]
    
    # inject in the 4D cube
    fcp_cube = cube_inject_companions(cube, psf, derot_angles, flevel, 
                                      plsc=1, rad_dists=[r], n_branches=1, 
                                      theta=theta, imlib=imlib, 
                                      interpolation=interpolation, 
                                      transmission=transmission, 
                                      verbose=verbose)

    return fcp_cube