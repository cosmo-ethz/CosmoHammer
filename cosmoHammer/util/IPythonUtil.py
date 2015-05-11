# Copyright (C) 2014 ETH Zurich, Institute for Astronomy

'''
Created on Jul 23, 2014

author: jakeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from IPython import parallel

class IPythonPoolWrapper(object):
    """
    Wraps the IPython balanced view to interface the Pool.map
    """
    
    def __init__(self):
        client = parallel.Client()
        self.view = client.load_balanced_view()
        
    def map(self, func, sequence):    
        return self.view.map_sync(func, sequence)
    
    def close(self):
        self.view.close()
