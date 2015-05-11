#!/usr/bin/env python
"""
Runs CosmoHammer with a likelihood module simulating the WMAP likelihood by assuming the parameter distributions to be gaussian.
Yields results very similar to ones gathered using CAMB and WMAP in default config, but only needs a fraction of the time.
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import numpy as np

from cosmoHammer import LikelihoodComputationChain
from cosmoHammer import CosmoHammerSampler
from cosmoHammer.util import InMemoryStorageUtil

from cosmoHammer.modules import PseudoCmbModule
from cosmoHammer.pso.ParticleSwarmOptimizer import ParticleSwarmOptimizer

#parameter start center, min, max, start width
params = np.array([[70, 40, 100, 3],
            [0.0226, 0.005, 0.1, 0.001],
            [0.122, 0.01, 0.99, 0.01],
            [2.1e-9, 1.48e-9, 5.45e-9, 1e-10],
            [0.96, 0.5, 1.5, 0.02],
            [0.09, 0.01, 0.8, 0.03],
            [1,0,2,0.4] ])

chain = LikelihoodComputationChain(params[:,1], params[:,2])
pseudoLikelihood = PseudoCmbModule()

chain.addLikelihoodModule(pseudoLikelihood)
chain.setup()

# find the best fit value and update our params knowledge
print("find best fit point")
pso = ParticleSwarmOptimizer(chain, params[:,1], params[:,2])
psoTrace = np.array([pso.gbest.position.copy() for _ in pso.sample()])
params[:, 0] = pso.gbest.position

storageUtil = InMemoryStorageUtil()
sampler = CosmoHammerSampler(
                params= params, 
                likelihoodComputationChain=chain, 
                filePrefix="temp/pseudoCmb_pso", 
                walkersRatio=50, 
                burninIterations=0, 
                sampleIterations=100,
                storageUtil=storageUtil,
                threadCount=4
                )

print("start sampling")
sampler.startSampling()
print("done!")

print("plotting")
import matplotlib.pyplot as plt
import triangle
data = storageUtil.samples
K = data.shape[1]
factor = 2.0 # size of one side of one panel
lbdim = 0.5 * factor # size of left/bottom margin
trdim = 0.2 * factor # size of top/right margin
whspace = 0.05 # w/hspace size
plotdim = factor * K + factor * (K - 1.) * whspace
dim = lbdim + plotdim + trdim

fig, ax = plt.subplots(K, K, figsize=(dim, dim), tight_layout=False)
triangle.corner(data, fig=fig)

for i in range(K):
    for j in range(i):
        ax[i, j].plot(psoTrace[:, j], psoTrace[:, i], "1-")


plt.show()