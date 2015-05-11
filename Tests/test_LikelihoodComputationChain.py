##!/usr/bin/env python
"""
Test the LikelihoodComputationChain module.

Execute with py.test -v

"""

import numpy
from cosmoHammer import LikelihoodComputationChain

class TestLikelihoodComputationChain(object):

    def test_modules(self):
        chain = LikelihoodComputationChain()
        
        assert len(chain.getCoreModules())==0
        assert len(chain.getLikelihoodModules())==0
        
        coreModule = DummyMoudle()
        likeModule = DummyMoudle()
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
        
        assert like == DummyMoudle.like
        assert len(data) == 1
        assert data["data"] == DummyMoudle.data
        
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
        assert like == -numpy.inf
        assert len(data) == 0
        
        like, data = chain([2, 3])
        assert like == -numpy.inf
        assert len(data) == 0
        
        
        
        
class DummyMoudle(object):
    
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