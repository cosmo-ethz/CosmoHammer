##!/usr/bin/env python
"""
Test the LikelihoodComputationChain module.

Execute with py.test -v

"""

import numpy as np
from cosmoHammer import LikelihoodComputationChain
from cosmoHammer.util import Params

class TestLikelihoodComputationChain(object):

    def test_modules(self):
        chain = LikelihoodComputationChain()
        
        assert len(chain.getCoreModules())==0
        assert len(chain.getLikelihoodModules())==0
        
        coreModule = DummyModule()
        likeModule = DummyModule()
        chain.addCoreModule(coreModule)
        chain.addLikelihoodModule(likeModule)
        assert len(chain.getCoreModules())==1
        assert len(chain.getLikelihoodModules())==1
        
        chain.setup()
        assert coreModule.init
        assert likeModule.init
        
        like, data = chain([0])
        
        assert coreModule.called
        assert likeModule.compLike
        
        assert like == DummyModule.like
        assert len(data) == 1
        assert data["data"] == DummyModule.data
        
    def test_isValid(self):
        chain = LikelihoodComputationChain()
        assert chain.isValid([0])

        chain = LikelihoodComputationChain(min=[0])
        assert chain.isValid([1])
        assert chain.isValid([0])
        assert not chain.isValid([-1])

        chain = LikelihoodComputationChain(min=[0, 1])
        assert chain.isValid([1, 2])
        assert chain.isValid([0, 1])
        assert not chain.isValid([-1, 1])
        assert not chain.isValid([0, 0])
        assert not chain.isValid([-1, 0])

        chain = LikelihoodComputationChain(max=[1])
        assert chain.isValid([1])
        assert chain.isValid([0])
        assert not chain.isValid([2])

        chain = LikelihoodComputationChain(max=[1, 2])
        assert chain.isValid([0, 1])
        assert chain.isValid([1, 2])
        assert not chain.isValid([2, 2])
        assert not chain.isValid([1, 3])
        assert not chain.isValid([2, 3])

        chain = LikelihoodComputationChain(min=[0, 1], max=[1, 2])
        assert chain.isValid([1, 2])
        assert chain.isValid([0, 1])
        assert chain.isValid([0, 1])
        assert chain.isValid([1, 2])
        assert not chain.isValid([-1, 1])
        assert not chain.isValid([0, 0])
        assert not chain.isValid([-1, 0])
        assert not chain.isValid([2, 2])
        assert not chain.isValid([1, 3])
        assert not chain.isValid([2, 3])
        
        like, data = chain([-1, 0])
        assert like == -np.inf
        assert len(data) == 0
        
        like, data = chain([2, 3])
        assert like == -np.inf
        assert len(data) == 0
        
    def test_createChainContext(self):
        chain = LikelihoodComputationChain()
        
        p = np.array([1,2])
        ctx = chain.createChainContext(p)
        assert ctx is not None
        assert np.all(ctx.getParams() == p)

    def test_createChainContext_params_invalid(self):
        chain = LikelihoodComputationChain()
        chain.values = []
        
        p = np.array([1,2])
        ctx = chain.createChainContext(p)
        
        assert ctx is not None
        assert np.all(ctx.getParams() == p)
        
    def test_createChainContext_params(self):
        keys = ["a", "b"]
        params = Params((keys[0], 0),
                        (keys[1], 1))
        chain = LikelihoodComputationChain()
        chain.params = params
        
        p = np.array([1,2])
        ctx = chain.createChainContext(p)
        
        assert ctx is not None
        assert np.all(ctx.getParams().keys == keys) 
        assert np.all(ctx.getParams()[0] == p[0]) 
        assert np.all(ctx.getParams()[1] == p[1]) 
        

        
class DummyModule(object):
    
    like = 0
    data = 1
    
    def __init__(self):
        self.init = False
        self.called = False
        self.compLike = False
    
    def setup(self):
        self.init = True
        
    def __call__(self, ctx):
        self.called = True
        ctx.getData()["data"] = self.data
        
    def computeLikelihood(self, ctx):
        self.compLike = True
        return self.like