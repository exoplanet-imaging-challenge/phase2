#! /usr/bin/env python

"""
Module with distance metrics routines used in the context of the Exoplanet 
Imaging Data Challenge
"""

__author__ = 'Valentin Christiaens'
__all__ = ['distance_L1',
           'distance_L2']

import numpy as np


def distance_L1(gts, estimates, norm=True):
    """ Function to estimate the goodness of an estimation, based on the 
    L1 norm distance between estimates and ground truths.

    Parameters
    ----------
    gts : numpy array
        Array with the ground truths
    estimates : numpy array
        Array with the estimates.
    norm: bool, optional
        Whether to scale the distance with ground truth value
        
    Returns
    -------
    dist : numpy array
        Array of distances.

    """
    
    if estimates.shape !=  gts.shape:
        raise TypeError("Provide identical format for estimates and gts.")

    dist = np.abs(gts-estimates)
    
    if norm:
        dist /= np.abs(gts)
        
    return dist



def distance_L2(gts, estimates, norm=False):
    """ Function to estimate the goodness of an estimation, based on the 
    L2 norm distance between estimates and ground truths.

    Parameters
    ----------
    gts : numpy array
        Array with the ground truths
    estimates : numpy array
        Array with the estimates.
    norm: bool, optional
        Whether to scale the distance with ground truth value
        
    Returns
    -------
    dist : numpy array
        Array of distances.

    """
    
    if estimates.shape !=  gts.shape:
        raise TypeError("Provide identical format for estimates and gts.")

       

    if norm:
        dist = np.sqrt(np.sum(np.power((gts-estimates)/gts, 2))) 
    else:
        dist = np.sqrt(np.sum(np.power(gts-estimates, 2)))

    return dist