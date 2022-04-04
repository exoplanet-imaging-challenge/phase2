#! /usr/bin/env python

"""
Module with routines used by EvalAI in the context of the Exoplanet Imaging 
Data Challenge
"""

__author__ = 'Carles Cantero, Valentin Christiaens'
__all__ = ['create_mefs',
           'read_submission',
           'eval_submission']


from metrics import distance
import numpy as np 
import zipfile
import vip_hci as vip
import warnings
import os
warnings.filterwarnings('ignore')


def create_mefs(n_mef, n_estimates, estimate_bounds=[0,1], error_bounds=[0,2], nsamp_posterior=1000, save_to='./', zipname='mef1.zip', mefname='mef'):
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
    ·  mef: str
         Common name for all MEF files created. Then, an numerical id is added to 
         differentiate among them.
    '''
    
    if not isinstance(n_mef, int):
        msg = 'n_mef must be an integer.'
        raise ValueError(msg)
    if not isinstance(n_estimates, int):
        msg = 'n_estimates must be an integer.'
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
    
    d_list=[]
    for i in range(n_mef):
        estimate = np.random.uniform(low=estimate_bounds[0], high=estimate_bounds[1], size=n_estimates)
        error    = np.random.uniform(low=error_bounds[0], high=error_bounds[1], size=n_estimates)
        post_list=[]
        for j in range(n_estimates):
            post = np.random.normal(loc=estimate[j], scale=error[j], size=nsamp_posterior)
            post_list.append(post)
        d = (estimate, error, np.array(post_list))
        d_list.append(d)
        
        if save_to:
            if not isinstance(save_to, str):
                msg = 'save_to must be an string.'
                raise ValueError(msg) 
            fitsname= str(save_to)+str(mefname)+str(i+1)+'.fits'
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
            fitsname= str(save_to)+str(mefname)+str(i+1)+'.fits'
            f.write(fitsname)
            os.remove(fitsname) 
            
    return d_list



def read_submission(zipfilename, fitsfilenames=None,  verbose=False):
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
                for i in fitsfilenames: file.extract(i, str(tempfolder))
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

    res = []
    for mef in names:
        if verbose: 
            print('File '+str(mef)+':')
        mef_ = mef.removesuffix('.fits')
        estimates    = np.asarray(vip.fits.open_fits(fitsfilename=str(tempfolder)+'/'+str(mef_), n=0, verbose=verbose))
        uncertanties = np.asarray(vip.fits.open_fits(fitsfilename=str(tempfolder)+'/'+str(mef_), n=1, verbose=verbose))
        posteriors   = np.asarray(vip.fits.open_fits(fitsfilename=str(tempfolder)+'/'+str(mef_), n=2, verbose=verbose))
        results = (estimates, uncertanties, posteriors)
        res.append(results)
    file.close()
    shutil.rmtree(str(tempfolder))
    
    return res



def eval_submission(username, astrometry, photometry, verbose=True, plot=True):
    '''
    Function to evaluate both the astrometry and photometry submissions 
    for the second Exoplanet Imaging Data Challenge.
    
     Parameters
    ----------
    ·  username: str
        The username of the submission participant.
    ·  astrometry: list
        List with the name of the two ZIP files to evaluate the astrometry task, 
        the submission and the ground_truth. 
        For example, astrometry=['submission.zip', 'ground_truth.zip']
    ·  photometry: list
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
    
    if not isinstance(username, str):
        msg = 'username must be a string.'
        raise ValueError(msg)

    
    # Read astrometry ZIP files
    if isinstance(astrometry, list):
        if all(isinstance(item, str) for item in astrometry):
            sub_astro = read_submission(zipfilename=str(astrometry[0]))
            gt_astro  = read_submission(zipfilename=str(astrometry[1]))
        else:
            msg = 'each item in astrometry must be an string.'
            raise ValueError(msg) 
    else:
        msg = 'astrometry must be a list or a None.'
        raise ValueError(msg) 
        
    
    # Read photometry ZIP files
    if isinstance(photometry, list):
        if all(isinstance(item, str) for item in photometry):
            sub_photo = read_submission(zipfilename=str(photometry[0]))
            gt_photo  = read_submission(zipfilename=str(photometry[1]))
        else:
            msg = 'each item in photometry must be an string.'
            raise ValueError(msg) 
    else:
        msg = 'photometry must be a list or a None.'
        raise ValueError(msg) 
    
    # Evaluate astrometry
    drs, dthetas = [], []
    for i in range(len(gt_astro)):
        r_sub, theta_sub = sub_astro[i][0]
        r_gt, theta_gt   = gt_astro[i][0]
        d_r     = distance(r_gt, r_sub, errors=None, mode='relative')
        d_theta = distance(theta_gt, theta_sub, errors=None, mode='relative')
        drs.append(d_r)
        dthetas.append(d_theta)
    metric_astro = np.mean([np.mean(drs), np.mean(d_theta)])
    if verbose:
        print('ASTROMETRY TASK')
        print('----------------')
        print(' > Distance per cube:')
        print('  · r='+str(np.round(drs,3)))
        print('  · \u03B8='+str(np.round(dthetas,3)))
        print(' > Final metric of '+str(username)+': ' +str(metric_astro))
        print()
        
    # Evaluate astrometry
    contrasts_avg = []
    for i in range(len(gt_photo)):
        sub_contrasts = sub_photo[i][0]
        gt_contrasts  = gt_photo[i][0]
        dcontrasts = []
        for j in range(len(gt_contrasts)):
            d_contrast = distance(gt_contrasts[j], sub_contrasts[j], errors=None, mode='relative')
            dcontrasts.append(d_contrast)
        contrasts_avg.append(np.mean(dcontrasts))
    metric_photo = np.mean(contrasts_avg)
    if verbose: 
        print('PHOTOMETRY TASK')
        print('----------------')
        print(' > Distance per cube:')
        print('  · Contrast= '+str(np.round(contrasts_avg, 3)))
        print(' > Final metric of '+str(username)+': ' +str(metric_photo))
        
    if plot:
        x = np.arange(0, len(gt_photo[0][0]))
        fig, axs = plt.subplots(2,9, figsize=(32,6))
        for i in range(len(gt_photo)):
            axs[0][i].set_title('Cube '+str(i+1), fontsize=15)
            sns.kdeplot(sub_astro[i][2][0], sub_astro[i][2][1], ax=axs[0][i], alpha=0.8, label='P($\hat{y}$)')
            axs[0][i].scatter(sub_astro[i][0][0],sub_astro[i][0][1], marker='X', c='k', label='$\hat{y}$')
            axs[0][i].scatter(gt_astro[i][0][0],gt_astro[i][0][1], marker='X', c='r', label='y')
            axs[0][i].grid(alpha=0.2)
            axs[0][i].set_xlabel('r [mas]', fontsize=14)
            if i==0: axs[0][i].set_ylabel('$\u03B8$ [º]', fontsize=14)
            axs[0][i].legend(loc=1)

            axs[1][i].plot(sub_photo[i][0], c='b', label='$\hat{y}$', linewidth=1)
            axs[1][i].plot(gt_photo[i][0], c='r', label='y', linewidth=1, linestyle='--')
            axs[1][i].fill_between(x, sub_photo[i][0]+sub_photo[i][1], sub_photo[i][0]-sub_photo[i][1], color='b', alpha=0.1, label='P($\hat{y}$)')
            axs[1][i].grid(alpha=0.2)
            axs[1][i].set_xlabel('Wavelength', fontsize=14)
            if i==0: axs[1][i].set_ylabel('Contrast', fontsize=14)
            axs[1][i].legend(loc=1)

        plt.subplots_adjust(top = 0.99, bottom=0.1, hspace=0.5, wspace=0.3)
        plt.show()
        
    return metric_astro, metric_photo
