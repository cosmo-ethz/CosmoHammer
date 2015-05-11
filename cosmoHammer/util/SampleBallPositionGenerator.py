
import numpy as np


class SampleBallPositionGenerator(object):
    """
        Generates samples in a very thight n-dimensional ball 
    """
    
    def setup(self, sampler):
        """
            setup the generator
        """
        self.sampler = sampler
    
    def generate(self):
        """
            generates the positions
        """
        
        return [self.sampler.paramValues+np.random.normal(size=self.sampler.paramCount)*self.sampler.paramWidths for i in range(self.sampler.nwalkers)]
    
    def __str__(self, *args, **kwargs):
        return "SampleBallPositionGenerator"