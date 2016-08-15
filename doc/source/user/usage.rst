========
Usage
========

General usage of CosmoHammer
-----------------------------

To run CosmoHammer in order to sample the WMAP 9 year likelihood, you would do something like:

::

    from cosmoHammer import MpiCosmoHammerSampler
    from cosmoHammer import LikelihoodComputationChain
	
    from wmap9Wrapper import WmapLikelihoodModule as wmap9
    from pycambWrapper import PyCambCoreModule

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
    
    chain.addCoreModule(PyCambCoreModule())
    
    chain.addLikelihoodModule(wmap9.WmapLikelihoodModule())
    
    chain.setup()
    
    sampler = MpiCosmoHammerSampler(
                params= params, 
                likelihoodComputationChain=chain, 
                filePrefix="cosmoHammerWmap9", 
                walkersRatio=50, 
                burninIterations=250, 
                sampleIterations=250)
                
    sampler.startSampling()


	