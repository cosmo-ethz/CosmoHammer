#!/usr/bin/env python
"""
Runs CosmoHammer with the CambWrapper and WMAPWrapper.
The CosmoHammer will sample with 50*7 Walker for 2*250 iterations.

"""
from cosmoHammer import MpiCosmoHammerSampler
from cosmoHammer import LikelihoodComputationChain
from cosmoHammer.util import Params

from wmap9Wrapper import WmapExtLikelihoodModule as wmap9
from cambWrapper import CambCoreModule


#parameter start center, min, max, start width
params = Params(("hubble",                [70, 65, 80, 3]),
                ("ombh2",                 [0.0226, 0.01, 0.03, 0.001]),
                ("omch2",                 [0.122, 0.09, 0.2, 0.01]),
                ("scalar_amp",            [2.1e-9, 1.8e-9, 2.35e-9, 1e-10]),
                ("scalar_spectral_index", [0.96, 0.8, 1.2, 0.02]),
                ("re_optical_depth",      [0.09, 0.01, 0.1, 0.03]),
                ("sz_amp",                [1,0,2,0.4]))

chain = LikelihoodComputationChain(
                    min=params[:,1], 
                    max=params[:,2])

camb = CambCoreModule.CambCoreModule()

chain.addCoreModule(camb)

chain.addLikelihoodModule(wmap9.WmapExtLikelihoodModule())

chain.setup()


sampler = MpiCosmoHammerSampler(
                params= params, 
                likelihoodComputationChain=chain, 
                filePrefix="cosmoHammerWmap9_", 
                walkersRatio=20, 
                burninIterations=0, 
                sampleIterations=50)

print("start sampling")
sampler.startSampling()
print("done!")