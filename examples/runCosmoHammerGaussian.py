#!/usr/bin/env python
"""
Runs CosmoHammer with a multivariant gaussian (50 dimensions).
"""

from cosmoHammer import CosmoHammerSampler
from cosmoHammer import LikelihoodComputationChain

from cosmoHammer.modules import MultivarianteGaussianModule

import numpy as np




# We'll sample a 4-dimensional Gaussian...
ndim = 4
# ...with randomly chosen mean position...
means = np.random.rand(ndim)

# ...and a positive definite, non-trivial covariance matrix.
cov  = 0.5-np.random.rand(ndim**2).reshape((ndim, ndim))
cov  = np.triu(cov)
cov += cov.T - np.diag(cov.diagonal())
cov  = np.dot(cov,cov)

# Invert the covariance matrix first.
icov = np.linalg.inv(cov)

params = [[0, -5, 5, 1] ]*ndim

params = np.array(params)

chain = LikelihoodComputationChain(params[:,1],params[:,2])

multivarianteGaussian = MultivarianteGaussianModule(icov, means)
chain.addLikelihoodModule(multivarianteGaussian)
chain.setup()

sampler = CosmoHammerSampler(
                params= params, 
                likelihoodComputationChain=chain, 
                filePrefix="multivariantGausian", 
                walkersRatio=50, 
                burninIterations=0, 
                sampleIterations=100,
                )

print("start sampling")
sampler.startSampling()
print("done!")