

class IterationStopCriteriaStrategy(object):
    """
        A very simple implementation of a stop criteria strategy which does not stop the sampling until the max iteration is reached.
    """
    
    def __init__(self):
        """
            default constructor
        """
        pass
        
    def setup(self, sampler):
        """
            setup the strategy
        """
        self.sampler = sampler
        
    def hasFinished(self):
        """
            always returns false
        """
        return False

    def __str__(self, *args, **kwargs):
        return "IterationStopCriteriaStrategy"