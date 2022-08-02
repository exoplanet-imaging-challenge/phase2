#! /usr/bin/env python

"""
Module with routines used by EvalAI in the context of the Exoplanet Imaging 
Data Challenge
"""

__author__ = 'Carles Cantero, Valentin Christiaens'
__all__ = ['create_mefs',
           'read_submission',
           'eval_submission']


from .metrics import distance
import numpy as np 
import zipfile
import vip_hci as vip
import warnings
import os
warnings.filterwarnings('ignore')


def create_mefs(n_mef, n_estimates, n_inj=1, estimate_bounds=[0,1], error_bounds=[0,2], nsamp_posterior=1000, save_to='./', zipname='mef1.zip', mefnames='mef'):
    '''
    Function that creates MEF files with mock data for the second Exoplanet Imaging Data Challenge. 
    
    Each MEF file has three extensions: the estimates, the uncertanties and the posterior distributions 
    of the estimates. Both the estimates and the uncertanties are randomly sampled from an Uniform 
    distribution. Instead, the posterior distributions are randomly sampled from a Gaussian distribution.
    
    Parameters
    ----------
    ·  n_mef: int
        Number of MEF files.
    ·  n_estimates: int
        Number of estimates.
    ·  estimate_bounds: list
        Inner and outer boundaries used for defining the Uniform distribution from where 
        the estimates are then randomly sampled.
    ·  error_bounds: list
        Inner and outer boundaries used for defining the Uniform distribution from where 
        the uncertanties are then randomly sampled.
    ·  nsamp_posterior: int
        Number of posterior observations randomly sampled from the Gaussian distribution.
        By default, nsamp_posterior=1000.
    ·  save_to: str
        (optional) Path to save the MEF files created.
    ·  zipname: str
        (optional)  Name of the ZIP file.
    ·  mefnames: str
         Common name for all MEF files created. Then, an numerical id is added to 
         differentiate among them.
    '''
    
    if not isinstance(n_mef, int):
        msg = 'n_mef must be an integer.'
        raise ValueError(msg)
    if not isinstance(n_estimates, int) and not isinstance(n_estimates, list):
        msg = 'n_estimates must be an integer or a list of integers.'
        raise ValueError(msg)
    if not isinstance(estimate_bounds, list):
        msg = 'estimate_bounds must be a list.'
        raise ValueError(msg)
    if not isinstance(error_bounds, list):
        msg = 'error_bounds must be a list.'
        raise ValueError(msg)
    if not isinstance(nsamp_posterior, int):
        msg = 'nsamp_posterior must be an integer.'
        raise ValueError(msg)
        
    if isinstance(mefnames, str):
        mefnames = [str(mefnames)] * n_mef
                
    if not isinstance(n_estimates, list):
        n_estimates = [n_estimates] * n_mef
        
    if  isinstance(n_inj, int):
        n_inj = [n_inj] * n_mef
    
    
    d_list=[]
    for i in range(n_mef):
        list_est, list_err, list_post = [], [], []
        for inj in range(n_inj[i]):
            #print(i, inj, n_estimates[i])
            estimate = np.random.uniform(low=estimate_bounds[0], high=estimate_bounds[1], size=n_estimates[i])
            error    = np.random.uniform(low=error_bounds[0], high=error_bounds[1], size=n_estimates[i])
            post_list=[]
            for j in range(n_estimates[i]):
                post = np.random.normal(loc=estimate[j], scale=error[j], size=nsamp_posterior)
                post_list.append(post)
            list_est.append(estimate)
            list_err.append(error)
            list_post.append(np.array(post_list))
            
        d = (np.array(list_est), np.array(list_err), np.array(list_post))
        d_list.append(d)
        
        if save_to:
            if not isinstance(save_to, str):
                msg = 'save_to must be an string.'
                raise ValueError(msg) 
            #fitsname= str(save_to)+str(mefname)+str(i+1)+'.fits'
            fitsname= str(save_to)+str(mefnames[i])
            vip.fits.write_fits(fitsfilename=fitsname, array=d, verbose=False)
        
    if zipname:
        if not isinstance(zipname, str):
            msg = 'zipname must be an string.'
            raise ValueError(msg) 
        if not save_to:
            msg = 'For generating a ZIP file, the save_to parameter must be used as path.'
            raise ValueError(msg) 
            
        f = zipfile.ZipFile(str(zipname), 'w')
        for i in range(n_mef): 
            fitsname= str(save_to)+str(mefnames[i])+'.fits'
            #fitsname= str(save_to)+str(mefname)+str(i+1)
            f.write(fitsname)
            os.remove(fitsname) 
            
    return d_list



def read_submission(zipfilename, fitsfilenames=None,  read_estimates=True, read_errors=True, read_posteriors=False,verbose=False):
    '''
    Function to read the ZIP file submitted by a participant of the data challenge.
    
    The ZIP file is extracted in a temporal folder that it is then removed.
    
    Parameters
    ----------
    ·  zipfilename: str
        Name of the ZIP file.
    ·  fitsfilenames: list 
        (optional).List of files to search for inside the ZIP file. If None, 
        all files in the ZIP are extracted.
    ·  verbose: boolean
        (optional) Show additional information.
        
    Returns
    -------
    ·  res [list]
        List of results with the format=[cube, extensions]. For example,
        res[0][0] indicates the first cube and first extension. We have three 
        extensions: the first is the estimates, the second the uncertanties and 
        the third the posteriors.
    '''
        
    if isinstance(zipfilename, str):
        file = zipfile.ZipFile(zipfilename)
    else:
        msg = 'zipfilename must be an string.'
        raise ValueError(msg)
        
    tempfolder = ctime()    
    os.mkdir(str(tempfolder))
    
    if fitsfilenames is not None:
        if isinstance(fitsfilenames, list):
            if all(isinstance(item, str) for item in fitsfilenames):
                for i in fitsfilenames: 
                    file.extract(i, str(tempfolder))
                names = fitsfilenames
            else:
                msg = 'each item in fitsfilenames must be an string.'
                raise ValueError(msg)
        else:
            msg = 'fitsfilenames must be a list or a None.'
            raise ValueError(msg) 
    else:
        file.extractall(str(tempfolder))
        names = file.namelist()

    est, errors, post = [], [], []
    for mef in names:
        if verbose: 
            print('File '+str(mef)+':')
        mef_ = mef.removesuffix('.fits')
        if read_estimates:
            estimates    = np.array(vip.fits.open_fits(fitsfilename=str(tempfolder)+'/'+str(mef_), n=0, verbose=verbose))
            est.append(estimates)
        if read_errors:
            uncertanties = np.array(vip.fits.open_fits(fitsfilename=str(tempfolder)+'/'+str(mef_), n=1, verbose=verbose))
            errors.append(uncertanties)
        if read_posteriors:
            posteriors   = np.array(vip.fits.open_fits(fitsfilename=str(tempfolder)+'/'+str(mef_), n=2, verbose=verbose))
            post.append(posteriors)
    file.close()
    shutil.rmtree(str(tempfolder))
    
    # returns
    if read_estimates:
        if read_errors:
            if read_posteriors:
                return est, errors, post
            else:
                return est, errors
        if read_posteriors:
            return est, post
        else:
            return est
    if not read_estimates:
        if read_errors:
            if read_posteriors:
                return errors, post
            else:
                return errors
        if read_posteriors:
            return post
        else:
            print('You should choose one return')
            
            
    
    return res


def eval_submission(zips_astrometry, zips_photometry, verbose=False):
    '''
    Function that evaluates both the astrometry and photometry task of a submission. 

     Parameters
    ------------
    ·  zips_astrometry: list
        List with the name of the two ZIP files to evaluate the astrometry task, 
        the submission and the ground_truth. 
        For example, astrometry=['submission.zip', 'ground_truth.zip']
    ·  zips_photometry: list
        List with the name of the two ZIP files to evaluate the photometry task, 
        the submission and the ground_truth. 
        For example, photometry=['submission.zip', 'ground_truth.zip']
    ·  verbose: boolean
        (optional) Show additional information.
        
    Returns
    -------
    ·  metric_astro: float
        Final distance metric for the astrometry task
    ·  metric_photo: float
        Final distance metric for the photometry task
    
    '''
    # Read ZIP files: Astrometry and Spectrophotometry for both the user and the GT
    gt_astro   = read_submission(zipfilename= zips_astrometry[0], read_estimates=True, read_errors=False)
    user_astro = read_submission(zipfilename= zips_astrometry[1], read_estimates=True, read_errors=False)
    gt_photo   = read_submission(zipfilename= zips_photometry[0], read_estimates=True, read_errors=False)
    user_photo = read_submission(zipfilename= zips_photometry[1], read_estimates=True, read_errors=False)
    
    # Evaluation
    astro_metric = eval_astro(array_user_astro=user_astro,  array_gt_astro=gt_astro)
    photo_metric = eval_photo(array_user_photo= user_photo, array_gt_photo= gt_photo)
    
    if verbose:
        print('- Astrometry = '+str(astro_metric))
        print('- Spectrophotometry = '+str(photo_metric))
    
    return astro_metric, photo_metric





def eval_astro(array_user_astro, array_gt_astro):
    '''
    Function that evaluates the astrometry of a submission. It returns 
    a distance metric (float) for the astrometry task. The closer to zero 
    the metric, the better the performance of the algorithm.
    
    To use this function, we recommend to use first the read_submission()
    method for reading the data loading the data into arrays.
    
    Parameters
    ----------
    ·  array_user_astro: numpy array
       Array with all astrometry estimates of the submission
    ·  array_gt_astro: numpy array
       Array with all astrometry ground truth to compare the submission
       
    Returns
    -------
    ·  metric_astro_user: Astrometry mean distance metric 
    '''
    
    list_dist_astro_cubes=[] 
    for i in range(len(array_gt_astro)):
        list_dist_astro_planets=[]
        for j in range(len(array_gt_astro[i])):
            dx_user, dy_user = array_user_astro[i][j]
            dx_gt, dy_gt     = array_gt_astro[i][j]

            #if dx_user==-1 and dy_user==-1:

            dist_x = distance(dx_gt, dx_user, errors=None, mode='relative')
            dist_y = distance(dy_gt, dy_user, errors=None, mode='relative')

            dist_astro_planet = np.mean([dist_x,dist_y])
            list_dist_astro_planets.append(dist_astro_planet)

        dist_astro_cube = np.mean(list_dist_astro_planets)   
        list_dist_astro_cubes.append(dist_astro_cube)

    metric_astro_user = np.mean(list_dist_astro_cubes)
    
    return metric_astro_user



def eval_photo(array_user_photo, array_gt_photo):
    '''
    Function that evaluates the spectrophotometry of a submission. It returns 
    a distance metric (float) for the spectrophotometry task. The closer to zero 
    the metric, the better the performance of the algorithm.
    
    To use this function, we recommend to use first the read_submission()
    method for reading the data loading the data into arrays.
    
    Parameters
    ----------
    ·  array_user_photo: numpy array
       Array with all astrometry estimates of the submission
    ·  array_gt_photo: numpy array
       Array with all astrometry ground truth to compare the submission
       
    Returns
    -------
    ·  metric_photo_user: Spectrophotometry mean distance metric 
    '''
    
    list_dcontrast_cube=[]
    for i in range(len(array_gt_photo)): # cube
        list_dist_photo_planets=[]

        list_dcontrast_planets=[]
        for j in range(len(array_gt_photo[i])): #injection
            curve_user = array_user_photo[i][j]
            curve_gt   = array_gt_photo[i][j]

            list_dcontrasts = []
            for k in range(len(curve_gt)): # band
                if curve_gt[k].ndim==1:
                    gt = curve_gt[k]
                if curve_gt[k].ndim==2:
                    gt = np.array([item for sublist in curve_gt[k] for item in sublist]) 
                dist_contrast = distance(gt[k], curve_user[k], errors=None, mode='relative')

                list_dcontrasts.append(dist_contrast)
            list_dcontrast_planets.append(np.mean(list_dcontrasts))
        list_dcontrast_cube.append(np.mean(list_dcontrast_planets))
    metric_photo_user = np.mean(list_dcontrast_cube)
    
    return metric_photo_user