##!/usr/bin/env python
"""
Test the TestSampleFileUtil module.

Execute with py.test -v

"""

from cosmoHammer.util import SampleBallPositionGenerator
from cosmoHammer.util import FlatPositionGenerator

class TestPositionGenerators(object):

    nwalkers = 10

    def setup(self):
        self.sampler = DummySampler([1,2], 2, [1,1], self.nwalkers)

    def test_SampleBallPositionGenerator(self):
        gen = SampleBallPositionGenerator()
        gen.setup(self.sampler)
        
        pos = gen.generate()
        assert pos is not None
        assert len(pos) == self.nwalkers
        
    def test_FlatPositionGenerator(self):
        gen = FlatPositionGenerator()
        gen.setup(self.sampler)
        
        pos = gen.generate()
        assert pos is not None
        assert len(pos) == self.nwalkers
        
class DummySampler(object):
    
    def __init__(self, paramValues, paramCount, paramWidths, nwalkers):
        self.paramValues = paramValues
        self.paramCount = paramCount
        self.paramWidths = paramWidths
        self.nwalkers = nwalkers