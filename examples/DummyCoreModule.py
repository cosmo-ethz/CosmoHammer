class DummyCoreModule(object):
    """
    Dummy Core Module for calculating the squares of parameters.
    """

    def __init__(self):
        """
        Constructor of the DummyCoreModule
        """
        pass
        
    def __call__(self, ctx):
        """
        Computes something and stores it in the context
        """
        # Get the parameters from the context
        p = ctx.getParams()

        # Calculate something
        squares = p**2
        # Add the result to the context using a unique key
        ctx.add('squares_key', squares)
        
        # Store derived parameters for post processing
        derived_parms = sum(squares) % 2
        ctx.getData()["derived_params_key"] = derived_parms

    def setup(self):
        """
        Sets up the core module.
        Tasks that need to be executed once per run
        """
        #e.g. load data from files
        
        print("DummyCoreModule setup done")