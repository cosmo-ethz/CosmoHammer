##!/usr/bin/env python
"""
Test the CosmoHammerSampler module.

Execute with py.test -v

"""
import numpy as np
import os
import tempfile

from cosmoHammer import LikelihoodComputationChain
from cosmoHammer.modules.PseudoCmbModule import PseudoCmbModule

from cosmoHammer.util.IterationStopCriteriaStrategy import IterationStopCriteriaStrategy

from cosmoHammer.CosmoHammerSampler import CosmoHammerSampler

from cosmoHammer.util import SampleBallPositionGenerator
from cosmoHammer.util import FlatPositionGenerator
from cosmoHammer.util import InMemoryStorageUtil
from cosmoHammer.util import SampleFileUtil

class TestCosmoHammerSampler(object):
    params = None
    sampler = None
    
    def setup(self):
        """
        Initialise some data vectors used for the comparisons by the other functions.
        """
        self.params = np.array([[70, 40, 100, 3],
            [0.0226, 0.005, 0.1, 0.001],
            [0.122, 0.01, 0.99, 0.01],
            [2.1e-9, 1.48e-9, 5.45e-9, 1e-10],
            [0.96, 0.5, 1.5, 0.02],
            [0.09, 0.01, 0.8, 0.03],
            [1,0,2,0.4] ])


        #the real means..
        means = [70.704, 0.02256, 0.1115, 2.18474E-09, 0.9688, 0.08920]
        
        # ...and non-trivial covariance matrix.
        cov  = np.array([[6.11E+00, 0, 0, 0, 0, 0],
                        [7.19E-04, 3.26E-07, 0, 0, 0, 0],
                        [-1.19E-02, -3.37E-07, 3.14E-05, 0, 0, 0],
                        [-3.56E-11, 1.43E-14, 1.76E-13, 5.96E-21, 0, 0],
                        [2.01E-02, 6.37E-06, -2.13E-05, 3.66E-13, 1.90E-04, 0],
                        [1.10E-02, 2.36E-06, -1.92E-05, 8.70E-13, 7.32E-05, 2.23E-04]])
        cov += cov.T - np.diag(cov.diagonal())
        
        # Invert the covariance matrix
        icov = np.linalg.inv(cov)
        
        chain = LikelihoodComputationChain()
        pseudoLikelihood = PseudoCmbModule(icov, means)
        
        chain.addLikelihoodModule(pseudoLikelihood)
        chain.setup()
        
        posGen = FlatPositionGenerator()
        
        self.sampler = CosmoHammerSampler(
                        params= self.params, 
                        likelihoodComputationChain=chain, 
                        filePrefix=self._getTempFilePrefix(), 
                        walkersRatio=10, 
                        burninIterations=1, 
                        sampleIterations=11,
                        initPositionGenerator=posGen,
                        storageUtil=InMemoryStorageUtil())
        
    def test_init(self):
        self.sampler = CosmoHammerSampler(
                params= self.params, 
                likelihoodComputationChain=LikelihoodComputationChain(), 
                filePrefix=self._getTempFilePrefix(), 
                walkersRatio=10, 
                burninIterations=1, 
                sampleIterations=1)
        
        assert isinstance(self.sampler.storageUtil, SampleFileUtil) 
        assert isinstance(self.sampler.stopCriteriaStrategy, IterationStopCriteriaStrategy)
        assert isinstance(self.sampler.initPositionGenerator, SampleBallPositionGenerator)
        assert self.sampler.likelihoodComputationChain.params is not None

    
    def test_no_burn_in(self):
        self.sampler.resetSampler()
        self.sampler.burninIterations = 0;
        self.sampler.startSampling()
        
        assert self.sampler.storageUtil.samplesBurnin == None
        assert self.sampler.storageUtil.probBurnin == None
    
    def test_one_iter_burn_in(self):
        self.sampler.resetSampler()
        self.sampler.burninIterations = 1;
        self.sampler.walkersRatio = 10;
        self.sampler.startSampling()
        
        assert self.sampler.storageUtil.samplesBurnin is not None
        assert self.sampler.storageUtil.probBurnin is not None

        params = 7
        samples = params * self.sampler.burninIterations * self.sampler.walkersRatio
        assert self.sampler.storageUtil.samplesBurnin.shape == (samples, params)
        assert self.sampler.storageUtil.probBurnin.shape == (samples, )
    
    def test_one_iter_sampling(self):
        self.sampler.resetSampler()
        self.sampler.burninIterations = 0;
        self.sampler.sampleIterations = 1;
        self.sampler.walkersRatio = 10;
        self.sampler.startSampling()
        
        params = 7
        samples = params * self.sampler.sampleIterations * self.sampler.walkersRatio
        
        assert self.sampler.storageUtil.samplesBurnin is None
        assert self.sampler.storageUtil.probBurnin is None
        assert self.sampler.storageUtil.samples.shape == (samples, params)
        assert self.sampler.storageUtil.prob.shape == (samples, )
    
    def _getTempFilePrefix(self):
        return os.path.join(tempfile.mkdtemp(), "pseudoCmb")