.. _api:

API
***

.. automodule:: cosmoHammer

This page details the methods and classes provided by the ``cosmoHammer`` module.


Samplers
--------

:mod:`CosmoHammerSampler` Module
===================================

Standard usage of ``CosmoHammer`` involves instantiating an
:class:`CosmoHammerSampler`.

.. autoclass:: cosmoHammer.CosmoHammerSampler
   :members: 


:mod:`MpiCosmoHammerSampler` Module
===================================

To distribute ``CosmoHammer`` in a cluster involves instantiating an
:class:`MpiCosmoHammerSampler`.

.. autoclass:: cosmoHammer.MpiCosmoHammerSampler
   :show-inheritance:

:mod:`ConcurrentMpiCosmoHammerSampler` Module
=============================================

To distribute ``CosmoHammer`` in a cluster and to spawn multiple processes involves instantiating an
:class:`ConcurrentMpiCosmoHammerSampler`.

.. autoclass:: cosmoHammer.ConcurrentMpiCosmoHammerSampler
   :members: 
   :show-inheritance:

CosmoHammer Chains
-------------------------------------

``CosmoHammer`` comes with a plain vanillia chain implementation	
:class:`LikelihoodComputationChain`.

.. autoclass:: cosmoHammer.LikelihoodComputationChain
   :members: 

.. autoclass:: cosmoHammer.ChainContext
   :members: 

CosmoHammer Exceptions
-------------------------------------

``CosmoHammer`` may raise the following exceptions while execution	

.. automodule:: cosmoHammer.exceptions
    :members:
    :undoc-members:
    :show-inheritance:


CosmoHammer Utils
-------------------------------------

.. autoclass:: cosmoHammer.util.Params
   :members: 

.. autoclass:: cosmoHammer.util.SampleBallPositionGenerator
   :members: 

.. autoclass:: cosmoHammer.util.FlatPositionGenerator
   :members: 

.. autoclass:: cosmoHammer.util.SampleFileUtil
   :members: 

.. autoclass:: cosmoHammer.util.InMemoryStorageUtil
   :members: 



ParticleSwarmOptimizer Package
------------------------------

:mod:`ParticleSwarmOptimizer` Module
====================================

.. autoclass:: cosmoHammer.ParticleSwarmOptimizer
   :members: 


:mod:`MpiParticleSwarmOptimizer` Module
=======================================

.. autoclass:: cosmoHammer.MpiParticleSwarmOptimizer
   :members: 

