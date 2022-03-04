#! /usr/bin/env python

"""
Module with distance metrics routines used in the context of the Exoplanet 
Imaging Data Challenge
"""

__author__ = 'Valentin Christiaens'
__all__ = ['distance']

import numpy as np


def distance(gts, estimates, errors=None, mode='relative'):
    """ Function to estimate the goodness of an estimation, based on the 
    simple distance between estimates and ground truths.

    Parameters
    ----------
    gts : numpy array
        Array with the ground truths
    estimates : numpy array
        Array with the estimates.
    errors : numpy array, optional
        Array with the uncertainties associated to each estimate
    mode: str, optional
        Sets the mode used to calculate the distance:
            - "relative": absolute difference scaled by ground truth value
        
    Returns
    -------
    distance : float
        Goodness of estimation.

    """
    
    if estimates.shape !=  gts.shape:
        raise TypeError("Provide identical format for estimates and gts.")
    if errors is not None:
        if errors.shape !=  estimates.shape:
            msg = "If provided, errors should have same shape as estimates"
            raise TypeError(msg)

    if mode == 'relative':
        distance = np.abs(gts-estimates)/np.abs(gts)

    return distance