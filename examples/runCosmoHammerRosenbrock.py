#!/usr/bin/env python
"""
Runs CosmoHammer with a rosenbrock density module
"""
from __future__ import print_function, division, absolute_import, unicode_literals

from cosmoHammer import CosmoHammerSampler
from cosmoHammer import LikelihoodComputationChain
from cosmoHammer.modules import RosenbrockModule

import numpy as np


#parameter start center, min, max, start width
params = [[1, -10, 10, 0.1],
                [1, -10, 10, 0.1]]



params = np.array(params)

chain = LikelihoodComputationChain()

rosenbrock = RosenbrockModule()

chain.addLikelihoodModule(rosenbrock)
chain.setup()


sampler = CosmoHammerSampler(
                params= params, 
                likelihoodComputationChain=chain, 
                filePrefix="temp/rosenbrock", 
                walkersRatio=50, 
                burninIterations=100, 
                sampleIterations=100)
sampler.startSampling()
