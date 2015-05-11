"""
Test the CosmoHammerSampler module.

Execute with py.test -v

"""
from __future__ import print_function, division, absolute_import, unicode_literals

from cosmoHammer.ChainContext import ChainContext

import numpy as np

class TestCosmoHammerSampler(object):
    ctx = None
    params = np.array([[1,2,3],[4,5,6]])
    
    def setup(self):
        self.ctx=ChainContext(self, self.params)
        
    def test_no_data(self):
        assert self.ctx.getParent() == self
        assert self.ctx.getParams() is self.params
        assert self.ctx.contains("key") == False
        assert self.ctx.getData() is not None
        assert len(list(self.ctx.getData().items())) == 0
    
    def test_add_data(self):
        assert self.ctx.contains("key") == False
        assert self.ctx.getData() is not None
        
        self.ctx.add("key", "value")
        
        assert self.ctx.contains("key") == True
        assert self.ctx.getData() is not None
        
        assert self.ctx.get("key") == "value"

    def test_remove_data(self):
        assert self.ctx.contains("key2") == False
        assert self.ctx.getData() is not None
        
        self.ctx.add("key2", "value")
        
        assert self.ctx.contains("key2") == True
        assert self.ctx.getData() is not None
        
        assert self.ctx.get("key2") == "value"
        
        self.ctx.remove("key2")
        assert self.ctx.contains("key2") == False

    def test_get_default(self):
        assert self.ctx.contains("aaa") == False
        assert self.ctx.get("aaa", "default") == "default"
        
        
    def test_additional_data(self):
        assert self.ctx.getData() is not None
        assert len(list(self.ctx.getData().items())) == 0
        
        self.ctx.getData()["moreData"] = "data"
        assert len(list(self.ctx.getData().items())) == 1