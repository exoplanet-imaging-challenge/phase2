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


def inject_fcp_ifs(cube, derot_angles, psf, rtheta_planet, planet_spec, 
                   star_obs_spec, star_mod_spec, mean_contrast, spec_res=None, 
                   transmission=None, norm_fac=None, imlib='vip-fft', 
                   interpolation=None, verbose=False, full_output=False):
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
    rtheta_planet: tuple of 2 floats
        (r, theta) polar coordinates for the fake companion to be injected. 
        These coordinates are to be provided for the derotated image - although 
        the injection is performed in the yet non-derotated cube. Theta is the
        trigonometric angle counted from the positive x-axis.
    planet_spec: 2D numpy array
        Spectrum to be injected. Dimensions should be (2 x n_channels),
        where the first dimension should provide the wavelengths in microns, 
        and the second the fluxes (arbitrary units). Does not necessarily have 
        to be resampled yet.
    star_obs_spec: 2D numpy array
        Spectrum of the star, as measured by the IFU. Dimensions should be 
        (2 x n_channels), where the first dimension should provide the 
        wavelengths in microns, and the second the fluxes (arbitrary units).
    star_mod_spec: 2D numpy array
        Model (or calibrated) spectrum of the star. Dimensions should be 
        (2 x n_channels), where the first dimension should provide the 
        wavelengths in microns, and the second the fluxes (arbitrary units).
    mean_contrast: float
        Requested mean contrast (over all channels) between the fake companion 
        and the star, used to scale the fluxes of the companion spectrum before
        injection.
    spec_res: float, optional
        Spectral resolution of the instrument. If provided, it is used to 
        convolve the fcp spectrum before resampling to the IFU wavelength 
        sampling.
    transmission: numpy array, optional
        Radial transmission of the coronagraph, if any. Array with 2 columns.
        First column is the radial separation in pixels. Second column is the
        corresponding off-axis transmission (between 0 and 1).
    norm_fac: numpy array, optional
        Vector of scaling/normalization factors to be applied to the injected 
        spectrum for each timestamp (i.e. should have the same length as 
        derot_angles). This can be used to take into account varying observing
        conditions or airmass.
    imlib : str, optional, {'vip-fft', 'opencv', 'ndimage-fourier'}
        Image library used for image shifts. See the documentation of the 
        ``vip_hci.preproc.frame_shift`` function.
    interpolation : str, optional
        Interpolation method used for image shifts. See the documentation of 
        the ``vip_hci.preproc.frame_shift`` function.
    verbose: bool, optional
        Whether to print more information during processing.
    full_output: bool, optional
        Whether to also return the fluxes of the injected planet.
    
    Returns
    -------
    fcp_cube : 4D numpy array
        Output IFS 4D master cube where the companion has been injected.
    [full_output=True]
    flevel : 1D numpy array
        Fluxes used for the injected planet
    """

    r, theta = rtheta_planet

    # convolve + resample the fcp model spectrum
    planet_spec_res = resample_model(star_obs_spec[0], planet_spec[0], 
                                     planet_spec[1], instru_res=spec_res)
    
    # convolve + resample the star model spectrum
    star_mod_spec_res = resample_model(star_obs_spec[0], star_mod_spec[0], 
                                       star_mod_spec[1], instru_res=spec_res)
    
    # find flux scaling factor
    ## instrumental+atm effects
    planet_spec = (star_obs_spec[1]/star_mod_spec_res[1])*planet_spec_res[1]
    ## contrast
    scal_fac = mean_contrast*np.sum(star_obs_spec[1])/np.sum(planet_spec)
    fluxes = scal_fac*planet_spec
    if verbose:
        msg = "Flux levels used for planet injection"
        msg+= " (before considering airmass): "
        print(msg, fluxes)
    
    # include the effect of airmass
    if norm_fac is not None:
        if len(norm_fac) != len(derot_angles):
            msg = "Normalization factors and derotation angles should have "
            msg += "same length."
            raise TypeError(msg)
        flevel = np.outer(fluxes, norm_fac)
    else:
        flevel = fluxes
    
    # inject in the 4D cube
    fcp_cube = cube_inject_companions(cube, psf, derot_angles, flevel, 
                                      plsc=1., rad_dists=[r], n_branches=1, 
                                      theta=theta, imlib=imlib, 
                                      interpolation=interpolation, 
                                      transmission=transmission, 
                                      verbose=verbose)
    if full_output:
        return fcp_cube, fluxes
    else:
        return fcp_cube