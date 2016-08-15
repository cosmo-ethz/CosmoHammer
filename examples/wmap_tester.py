#!/usr/bin/env python
"""
Calls the CambWrapper and WmapWrapper

"""
from __future__ import print_function, division, absolute_import, unicode_literals

from wmap3Wrapper import WmapLikelihoodModule as wmap3
from wmap5Wrapper import WmapLikelihoodModule as wmap5
from wmap7Wrapper import WmapLikelihoodModule as wmap7
from wmap9Wrapper import WmapLikelihoodModule as wmap9
from pycambWrapper import PyCambCoreModule
from cambWrapper import CambCoreModule

from cosmoHammer.ChainContext import ChainContext


pyCambCore = PyCambCoreModule.PyCambCoreModule()
cambCore = CambCoreModule()
wmap3Likelihood = wmap3.WmapLikelihoodModule()
wmap5Likelihood = wmap5.WmapLikelihoodModule()
wmap7Likelihood = wmap7.WmapLikelihoodModule()
wmap9Likelihood = wmap9.WmapLikelihoodModule()
#setting up wrappers
cambCore.setup()
pyCambCore.setup()

wmap3Likelihood.setup()
wmap5Likelihood.setup()
wmap7Likelihood.setup()
wmap9Likelihood.setup()

#camb wrapper
print("setup done. calling CAMB power spectrum computation")

paramValues = [70, 0.0226, 0.122, 2.1E-009, 0.96, 0.09]

ctx = ChainContext(None, paramValues)
cambCore(ctx)

print("cls computation done. calling WMAP likelihood")
print("Likelihood WMAP 3: %s"%wmap3Likelihood.computeLikelihood(ctx))
print("Likelihood WMAP 5: %s"%wmap5Likelihood.computeLikelihood(ctx))
print("Likelihood WMAP 7: %s"%wmap7Likelihood.computeLikelihood(ctx))
print("Likelihood WMAP 9: %s"%wmap9Likelihood.computeLikelihood(ctx))

#pycamb
ctx = ChainContext(None, paramValues)
pyCambCore(ctx)

print("cls computation done. calling WMAP likelihood")
print("Likelihood WMAP 3: %s"%wmap3Likelihood.computeLikelihood(ctx))
print("Likelihood WMAP 5: %s"%wmap5Likelihood.computeLikelihood(ctx))
print("Likelihood WMAP 7: %s"%wmap7Likelihood.computeLikelihood(ctx))
print("Likelihood WMAP 9: %s"%wmap9Likelihood.computeLikelihood(ctx))

