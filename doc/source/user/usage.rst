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
    params = np.array(
            [[70, 40, 100, 3],
            [0.0226, 0.005, 0.1, 0.001],
            [0.122, 0.01, 0.99, 0.01],
            [2.1e-9, 1.48e-9, 5.45e-9, 1e-10],
            [0.96, 0.5, 1.5, 0.02],
            [0.09, 0.01, 0.8, 0.03],
            [1,0,2,0.4] ])
    
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


	