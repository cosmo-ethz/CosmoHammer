class DummyLikelihoodModule(object):
    """
    Dummy object for calculating a likelihood
    """

    def __init__(self):
        """
        Constructor of the DummyLikelihoodModule
        """
        pass
    
    def computeLikelihood(self, ctx):
        """
        Computes the likelihood using information from the context
        """
        # Get information from the context. This can be results from a core
        # module or the parameters coming from the sampler
        squares = ctx.get('squares_key')
        
        # Calculate a likelihood up to normalization
        lnprob = -sum(squares)/2.0
        
        # Return the likelihood
        return lnprob
    
    def setup(self):
        """
        Sets up the likelihood module.
        Tasks that need to be executed once per run
        """
        #e.g. load data from files
        
        print("DummyLikelihoodModule setup done")
            
        
    