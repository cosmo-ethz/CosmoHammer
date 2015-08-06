from __future__ import print_function, division, absolute_import, unicode_literals
from cosmoHammer import getLogger

class RosenbrockModule(object):
    """
    A module for the computation of the rosenbrock likelihood
    """
    
    def __init__(self):
        self.a1 = 100.0
        self.a2 = 20.0

    def computeLikelihood(self, ctx):
        p = ctx.getParams()
        return -(self.a1 * (p.y - p.x**2)**2 + (1 - p.x)**2) / self.a2
    
    def setup(self):
        getLogger().info("Rosenbrock setup")