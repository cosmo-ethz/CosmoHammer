
import numpy as np


class FlatPositionGenerator(object):
    """
        Generates samples in a flat random space using
        center + (random values * 2 -1) * width
    """
    
    def __init__(self):
        """
            default constructor
        """
        pass

    def setup(self, sampler):
        """
            setup the generator
        """
        self.sampler = sampler
    
    def generate(self):
        """
            generates the positions
        """
        
        return [self.sampler.paramValues+(np.random.rand(self.sampler.paramCount)*2-1)*self.sampler.paramWidths for i in range(self.sampler.nwalkers)]
    
    def __str__(self, *args, **kwargs):
        return "FlatPositionGenerator"