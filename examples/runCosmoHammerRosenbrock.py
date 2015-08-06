#!/usr/bin/env python
"""
Runs CosmoHammer with a rosenbrock density module
"""
from __future__ import print_function, division, absolute_import, unicode_literals

from cosmoHammer import CosmoHammerSampler
from cosmoHammer import LikelihoodComputationChain
from cosmoHammer.modules import RosenbrockModule

from cosmoHammer.util import Params

#parameter start center, min, max, start width
params = Params(("x", [1, -10, 10, 0.1]),
                ("y", [1, -10, 10, 0.1]))



chain = LikelihoodComputationChain()

rosenbrock = RosenbrockModule()

chain.addLikelihoodModule(rosenbrock)
chain.setup()


sampler = CosmoHammerSampler(
                params= params, 
                likelihoodComputationChain=chain, 
                filePrefix="rosenbrock", 
                walkersRatio=50, 
                burninIterations=100, 
                sampleIterations=100)
sampler.startSampling()

try:
    import numpy as np
    import matplotlib.pyplot as plt
    data = np.loadtxt("rosenbrock.out")
    plt.scatter(data[:,0], data[:, 1], 1)
    plt.xlabel(params.keys[0])
    plt.ylabel(params.keys[1])
    plt.show()
except Exception:
    print("Plotting failed. Missing libs?")