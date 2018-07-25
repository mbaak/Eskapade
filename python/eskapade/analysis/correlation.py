"""Project: Eskapade - A python-based package for data analysis.

Created: 2018/06/23

Description:
    Convert Pearson correlation value into a chi2 value of a contingency test 
    matrix of a bivariate gaussion, and vice-versa. 
    Calculation uses scipy's mvn library.

Authors:
    KPMG Advanced Analytics & Big Data team, Amstelveen, The Netherlands

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms listed in the file
LICENSE.
"""

import numpy as np
from scipy.stats import mvn
from scipy import optimize

def _mvn_un(rho,lower,upper):
    '''Perform integral of bivariate normal gauss with correlation

    Integral is performed using scipy's mvn library.
    
    :returns float: integral value
    '''
    mu = np.array([0., 0.])
    S = np.array([[1.,rho],[rho,1.0]])
    p,i = mvn.mvnun(lower,upper,mu,S)
    return p

def _mvn_array(rho, sx, sy):
    '''Array of integrals over bivariate normal gauss with correlation

    Integrals are performed using scipy's mvn library.
    
    :returns list: list of integral values
    '''
    corr = []
    for i in range(len(sx)-1):
        for j in range(len(sy)-1):
            lower = [sx[i],sy[j]]
            upper = [sx[i+1],sy[j+1]]
            p = _mvn_un(rho,lower,upper)
            corr.append(p)
    return corr

def chi2_from_rho(rho, n, subtract_from_chi2=0, corr0=None, sx=None, sy=None, nx=-1, ny=-1):
    '''Calculate chi2-value of bivariate gauss having correlation value rho
    
    Calculate no-noise chi2 value of bivar gauss with correlation rho,
    with respect to bivariate gauss without any correlation.
    
    :returns float: chi2 value    
    '''
    assert nx>1 or sx is not None, 'number of bins along x-axis is unknown'
    assert ny>1 or sy is not None, 'number of bins along y-axis is unknown'
    if sx is None:
        sx = np.linspace(-5,5,nx+1)
    if sy is None:
        sy = np.linspace(-5,5,ny+1)
    if corr0 is None:
        corr0 = _mvn_array(0, sx, sy)
    corrr = _mvn_array(rho, sx, sy)
    chi2 = n * sum([((cr-c0)*(cr-c0)) / c0 for c0,cr in zip(corr0,corrr)])
    return chi2 - subtract_from_chi2

def rho_from_chi2(chi2, n, nx, ny, sx=None, sy=None):
    '''correlation coefficient of bivariate gaussian derived from chi2-value
    
    Chi2-value gets converted into correlation coefficient of bivariate gauss
    with correlation value rho, assuming giving binning and number of records. 
    Correlation coefficient value is between 0 and 1.

    Bivariate gaussian's range is set to [-5,5] by construction.

    :returns float: correlation coefficient
    '''
    assert nx>1 or sx is not None, 'number of bins along x-axis is unknown'
    assert ny>1 or sy is not None, 'number of bins along y-axis is unknown'
    if sx is None:
        sx = np.linspace(-5,5,nx+1)
    if sy is None:
        sy = np.linspace(-5,5,ny+1)
    corr0 = _mvn_array(0, sx, sy)
    rho = optimize.brentq(chi2_from_rho, 0, 1, args=(n, chi2, corr0, sx, sy))
    return rho
