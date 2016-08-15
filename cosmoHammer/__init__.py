import logging

# Author:  Joel Akeret
# Contact: jakeret@phys.ethz.ch
"""
This is the CosmoHammer package.
"""

__version__   = '0.6.0'
__author__    = 'Joel Akeret'
__credits__   = 'Institute for Astronomy ETHZ, Institute of 4D Technologies FHNW'

def getLogger():
    return logging.getLogger(__name__)


from cosmoHammer.CosmoHammerSampler import CosmoHammerSampler
from cosmoHammer.MpiCosmoHammerSampler import MpiCosmoHammerSampler
from cosmoHammer.ConcurrentMpiCosmoHammerSampler import ConcurrentMpiCosmoHammerSampler

from cosmoHammer.LikelihoodComputationChain import LikelihoodComputationChain
from cosmoHammer.ChainContext import ChainContext

from cosmoHammer.pso.ParticleSwarmOptimizer import ParticleSwarmOptimizer
from cosmoHammer.pso.MpiParticleSwarmOptimizer import MpiParticleSwarmOptimizer
