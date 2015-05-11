from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np
from cosmoHammer import getLogger

class MultivarianteGaussianModule(object):
    """
    Chain for computing the likelihood of a multivariante gaussian distribution
    """
    def __init__(self, icov, mu):
        self.icov = icov
        self.mu = mu
    
    
    def computeLikelihood(self, ctx):
        x = ctx.getParams()
        diff = x-self.mu
        return -np.dot(diff,np.dot(self.icov,diff))/2.0

    def setup(self):
        getLogger().info("Multivariante Gaussian setup")
            
        
    