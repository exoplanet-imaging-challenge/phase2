#! /usr/bin/env python

"""
Module with routines used by EvalAI in the context of the Exoplanet Imaging 
Data Challenge
"""

__author__ = 'Carles Cantero, Valentin Christiaens'
__all__ = ['read_entry',
           'eval_entry']


from .metrics import distance

def read_entry(zipfile):
    """ Function to read and extract results from a participant.

    Parameters
    ----------
    zipfile : str
        Full path + name of the zipfile.
        
    Returns
    -------
    res: ***

    """

    # read zipfile
    
    # assign values to res
    
    return res
    


def eval_entry(results):
    """ Function to evaluate the distances associated to the results contained
    in a proposed entry, to be returned to the leaderboard.

    Parameters
    ----------
    results : 
        
    Returns
    -------
    evals :

    """

    evals = []

    # compute different distances to be shown in leaderboard

    eval_main = distance(results)

    # update ranking
    
    
    return tuple(evals)