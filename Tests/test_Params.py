# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Aug 5, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from cosmoHammer.util import Params
import pytest
import numpy as np
class TestParams(object):
    
    def test_attr_looup(self):
        params = Params(("attr1", 1),
                        ("attr2", 2))
        
        assert params.attr1 == 1
        assert params.attr2 == 2
        
        with pytest.raises(AttributeError):
            params.inexistent
            
    def test_get(self):
        params = Params(("attr1", 1),
                        ("attr2", 2))
        
        assert params.get("attr1") == 1
        assert params.get("attr2") == 2
        
        with pytest.raises(KeyError):
            params.get("inexistent")
        
    def test_params_access_1d(self):
        values = [1,2]
        params = Params(("attr1", values[0]),
                        ("attr2", values[1]))
        
        assert np.all(params.values == values)

    def test_params_access_2d(self):
        values = np.array([[1,2,3,4],
                           [5,6,7,8]])
        params = Params(("attr1", values[0]),
                        ("attr2", values[1]))
        
        assert np.all(params.values == values)

        
    def test_slicing(self):
        values = np.array([[1,2,3,4],
                           [5,6,7,8]])
        params = Params(("attr1", values[0]),
                        ("attr2", values[1]))
        
        assert np.all(values[0] == values[0])
        assert np.all(values[:, 1] == values[:, 1])
        
    def test_names_access(self):
        keys = ["attr1","attr2"]
        params = Params((keys[0], 1),
                        (keys[1], 2))
        
        assert np.all(params.keys == keys)
        
    def test_names_immutability(self):
        keys = ["attr1","attr2"]
        params = Params((keys[0], 1),
                        (keys[1], 2))
        
        params.keys.append("irrelevant")
        
        assert np.all(params.keys == keys)
        
        
    def test_copy(self):
        params = Params(("attr1", 1),
                        ("attr2", 2))
        
        params2 = params.copy()
        
        assert np.all(params.keys == params2.keys)
        assert np.all(params.values == params2.values)
        
    def test_str(self):
        params = Params(("attr1", 1))
        s = str(params)
        assert "=" in s
        
    def test_value_assignment(self):
        values = np.array([[1,2,3,4],
                           [5,6,7,8]])
        params = Params(("attr1", values[0]),
                        ("attr2", values[1]))

        params[:,0] = 0
        assert np.all(params[:,0] == 0)

    def test_duplicated_key(self):
        with pytest.raises(KeyError):
            _ = Params(("attr1", 1),
                            ("attr1", 2))
        
        