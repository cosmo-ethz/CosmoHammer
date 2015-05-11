#Created on Nov 11, 2013
#author: jakeret


class LikelihoodComputationException(Exception):
    '''
    Exception for likelihood computation
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
class InvalidLikelihoodException(LikelihoodComputationException):
    """
    Exception for invalid likelihoods e.g. -loglike >= 0.0
    """
    
    def __init__(self, params=None):
        self.params = params
        
