from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from cosmoHammer import getLogger


#the real means..
WMAP7_MEANS = [70.704, 0.02256, 0.1115, 2.18474E-09, 0.9688, 0.08920]

# ...and non-trivial covariance matrix.
_cov  = np.array([[6.11E+00, 0, 0, 0, 0, 0],
                [7.19E-04, 3.26E-07, 0, 0, 0, 0],
                [-1.19E-02, -3.37E-07, 3.14E-05, 0, 0, 0],
                [-3.56E-11, 1.43E-14, 1.76E-13, 5.96E-21, 0, 0],
                [2.01E-02, 6.37E-06, -2.13E-05, 3.66E-13, 1.90E-04, 0],
                [1.10E-02, 2.36E-06, -1.92E-05, 8.70E-13, 7.32E-05, 2.23E-04]])
_cov += _cov.T - np.diag(_cov.diagonal())

# Invert the covariance matrix
WMAP7_ICOV = np.linalg.inv(_cov)


class PseudoCmbModule(object):
    """
    Chain for computing the likelihood of a multivariante gaussian distribution
    """
    def __init__(self, icov=WMAP7_ICOV, mu=WMAP7_MEANS, min_sz=0, max_sz=2):
        self.icov = icov
        self.mu = mu
        self.a = min_sz
        self.b = max_sz
    
    
    def computeLikelihood(self, ctx):
        x = ctx.getParams()

        diff = x[:6]-self.mu
        
        lnprob = -np.dot(diff,np.dot(self.icov,diff))/2.0

        lnprob -= np.log(self.b-self.a)
        return lnprob
    
    def setup(self):
        getLogger().info("Pseudo cmb setup")
            
        
    