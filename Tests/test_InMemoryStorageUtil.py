##!/usr/bin/env python
"""
Test the CosmoHammerSampler module.

Execute with py.test -v

"""
from cosmoHammer.util.InMemoryStorageUtil import InMemoryStorageUtil

import numpy as np

class TestCosmoHammerSampler(object):
    storageUtil = None
    samples = np.array([[1,2,3],[4,5,6]])
    prob = np.array([1,1])
    
    def setup(self):
        self.storageUtil=InMemoryStorageUtil()
        
    def test_no_data(self):
        
        assert self.storageUtil.samplesBurnin == None
        assert self.storageUtil.probBurnin == None
    
    def test_persistBurninValues(self):
        self.storageUtil.persistBurninValues(self.samples, self.prob, [])
        
        assert self.storageUtil.samplesBurnin is not None
        assert self.storageUtil.probBurnin is not None
        assert self.storageUtil.samplesBurnin.shape == (2, 3)
        assert self.storageUtil.probBurnin.shape == (2, )
    
        self.storageUtil.persistBurninValues(self.samples, self.prob, [])
        
        assert self.storageUtil.samplesBurnin is not None
        assert self.storageUtil.probBurnin is not None
        assert self.storageUtil.samplesBurnin.shape == (4, 3)
        assert self.storageUtil.probBurnin.shape == (4, )
    
    def test_persistSamplingValues(self):
        self.storageUtil.persistSamplingValues(self.samples, self.prob, [])
        
        assert self.storageUtil.samples is not None
        assert self.storageUtil.prob is not None
        assert self.storageUtil.samples.shape == (2, 3)
        assert self.storageUtil.prob.shape == (2, )
    
        self.storageUtil.persistSamplingValues(self.samples, self.prob, [])
        
        assert self.storageUtil.samples is not None
        assert self.storageUtil.prob is not None
        assert self.storageUtil.samples.shape == (4, 3)
        assert self.storageUtil.prob.shape == (4, )
    
