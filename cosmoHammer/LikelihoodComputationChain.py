from __future__ import print_function, division, absolute_import, unicode_literals
import numpy as np
from collections import deque
import os

from cosmoHammer.ChainContext import ChainContext
from cosmoHammer.exceptions import LikelihoodComputationException
from cosmoHammer import getLogger
from cosmoHammer.util import Params

class LikelihoodComputationChain(object):
    """
    Implementation of a likelihood computation chain.
    """

    def __init__(self, min=None, max=None):
        """
        Constructor for the likelihood chain

        :param min: array 
            lower bound for the parameters
        :param max: array
            upper bound for the parameters
        """
        self.min = min
        self.max = max
        self._likelihoodModules = deque();
        self._coreModules = deque();
            

    def getCoreModules(self):
        """pointer to the likelihood module list """
        return self._coreModules

    def getLikelihoodModules(self):
        """pointer to the core module list """
        return self._likelihoodModules

    def addLikelihoodModule(self, module):
        """
        adds a module to the likelihood module list
        
        :param module: callable
            the callable module to add for the likelihood computation
        """
        self.getLikelihoodModules().append(module)
        
    def addCoreModule(self, module):
        """
        adds a module to the likelihood module list
        
        :param module: callable
            the callable module to add for the computation of the data
        """
        self.getCoreModules().append(module)
        
        
    def isValid(self, p):
        """
        checks if the given parameters are valid 
        """
        if(self.min is not None):
            for i in range(len(p)):
                if (p[i]<self.min[i]):
                    getLogger().debug("Params out of bounds i="+str(i)+" params "+str(p))
                    return False
        
        if(self.max is not None):
            for i in range(len(p)):
                if (p[i]>self.max[i]):
                    getLogger().debug("Params out of bounds i="+str(i)+" params "+str(p))
                    return False
        
        return True

    
    def setup(self):
        """sets up the chain and its modules """
        for cModule in self.getCoreModules():
            cModule.setup()
            
        for cModule in self.getLikelihoodModules():
            cModule.setup()
            
    
    def __call__(self, p):
        """
        Computes the log likelihood by calling all the core and likelihood modules.
        
        :param p: the parameter array for which the likelihood should be evaluated
        
        :return: the current likelihood and a dict with additional data
        """
        try:
            getLogger().debug("pid: %s, processing: %s"%(os.getpid(), p))
            if not self.isValid(p):
                raise LikelihoodComputationException()
            
            ctx = self.createChainContext(p)
    
            self.invokeCoreModules(ctx)
    
            likelihood = self.computeLikelihoods(ctx)
            getLogger().debug("pid: %s, processed. Returning: %s"%(os.getpid(), likelihood))
            return likelihood, ctx.getData()
        except LikelihoodComputationException:
            getLogger().debug("pid: %s, processed. Returning: %s"%(os.getpid(), -np.inf))
            return -np.inf, []
    
    def createChainContext(self, p):
        """
        Returns a new instance of a chain context 
        """
        try:
            p = Params(*zip(self.params.keys, p))
        except Exception:
            # no params or params has no keys
            pass
        return ChainContext(self, p)
    
    def invokeCoreModules(self, ctx):
        """
        Iterates thru the core modules and invokes them
        """
        for cModule in self.getCoreModules():
            self.invokeCoreModule(cModule, ctx)
            
    
    def invokeCoreModule(self, coreModule, ctx):
        """
        Invokes the given module with the given ChainContext
        """
        coreModule(ctx)
        
    
    def computeLikelihoods(self, ctx):
        """
        Computes the likelihoods by iterating thru all the modules.
        Sums up the log likelihoods.
        """
        likelihood = 0
        
        for lModule in self.getLikelihoodModules():
            likelihood += self.invokeLikelihoodModule(lModule, ctx)

        return likelihood
    
    def invokeLikelihoodModule(self, likelihoodModule, ctx):
        """
        Invokes the given module with the given ChainContext
        """
        return likelihoodModule.computeLikelihood(ctx)
    
    def __str__(self, *args, **kwargs):
        s = "Core Modules: \n  "
        s = s + "\n  ".join([type(o).__name__ for o in self.getCoreModules()])

        s = s + "\nLikelihood Modules: \n  "
        s = s + "\n  ".join([type(o).__name__ for o in self.getLikelihoodModules()])
        return s
