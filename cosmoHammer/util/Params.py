# Copyright (C) 2015 ETH Zurich, Institute for Astronomy

'''
Created on Aug 5, 2015

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals

from copy import copy

import numpy as np


class Params(object):
    """
    A key-value parameter store preserving the order of the params passed to the intializer.

    Examples::
    
        $ params = Params(("key1", [1,2,3]),
                          ("key2", [1,2,3]))
    
        $ print(params.keys)
        > ['key1', 'key2']
        
        $ print(params.key1)
        > [1, 2, 3]
        
        $ params[:,0] = 0
        
        $ print(params.values)
        > [[0 2 3]
           [0 2 3]]
           
        $ print(params[:,1])
        > [2 2]
        
    """
    
    def __init__(self, *args):

        values = []
        self._keys = []
        for k,v in args:
            if k in self._keys:
                raise KeyError("Duplicated key '%s'"%k)
            
            self.__dict__[k] = v
            self._keys.append(k)
            values.append(v)
        self._values = np.array(values) 
        
    def __getitem__(self, slice):
        return self.values[slice]
    
    def __setitem__(self, slice, value):
        self.values[slice] = value
    
    def __str__(self):
        return ",".join(("%s=%s"%(k,v) for k,v in zip(self.keys, self.values)))
    
    @property
    def keys(self):
        return copy(self._keys)

    @property
    def values(self):
        return self._values
    
    def get(self, key):
        return self.__dict__[key]
    
    def copy(self):
        return Params(*zip(self.keys, self.values))