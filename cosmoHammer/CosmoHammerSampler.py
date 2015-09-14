from __future__ import print_function, division, absolute_import, unicode_literals

import emcee
import numpy as np
import logging
import time

import cosmoHammer
import cosmoHammer.Constants as c

from cosmoHammer import getLogger
from cosmoHammer.util import SampleFileUtil
from cosmoHammer.util import SampleBallPositionGenerator
from cosmoHammer.util.IterationStopCriteriaStrategy import IterationStopCriteriaStrategy



class CosmoHammerSampler(object):
    """
    A complete sampler implementation taking care of correct setup, chain burn in and sampling.

    :param params: the parameter of the priors
    :param likelihoodComputationChain: the callable computation chain
    :param filePrefix: the prefix for the log and output files
    :param walkersRatio: the ratio of walkers and the count of sampled parameters
    :param burninIterations: number of iteration for burn in
    :param sampleIterations: number of iteration to sample
    :param stopCriteriaStrategy: the strategy to stop the sampling. 
        Default is None an then IterationStopCriteriaStrategy is used
    :param initPositionGenerator: the generator for the init walker position. 
        Default is None an then SampleBallPositionGenerator is used
    :param storageUtil: util used to store the results
    :param threadCount: The count of threads to be used for the computation. Default is 1
    :param reuseBurnin: Flag if the burn in should be reused. 
        If true the values will be read from the file System. Default is False

    """

    def __init__(self, params, likelihoodComputationChain, filePrefix, walkersRatio, burninIterations, 
                 sampleIterations, stopCriteriaStrategy=None, initPositionGenerator=None, 
                 storageUtil=None, threadCount=1, reuseBurnin=False, logLevel=logging.INFO, pool=None):
        """
        CosmoHammer sampler implementation

        """
        self.params = params
        self.likelihoodComputationChain = likelihoodComputationChain
        self.walkersRatio = walkersRatio
        self.reuseBurnin = reuseBurnin
        self.filePrefix = filePrefix
        self.threadCount = threadCount
        self.paramCount = len(self.paramValues)
        self.nwalkers = self.paramCount*walkersRatio
        self.burninIterations = burninIterations
        self.sampleIterations = sampleIterations
        
        assert likelihoodComputationChain is not None, "The sampler needs a chain"
        assert sampleIterations > 0, "CosmoHammer needs to sample for at least one iterations"
        
        if not hasattr(self.likelihoodComputationChain, "params"):
            self.likelihoodComputationChain.params = params
        
        # setting up the logging
        self._configureLogging(filePrefix+c.LOG_FILE_SUFFIX, logLevel)
        
        if self.isMaster(): self.log("Using CosmoHammer "+str(cosmoHammer.__version__))
        
        # The sampler object
        self._sampler = self.createEmceeSampler(likelihoodComputationChain, pool=pool)
        
        if(storageUtil is None):
            storageUtil = self.createSampleFileUtil()
            
        self.storageUtil = storageUtil

        if(stopCriteriaStrategy is None):
            stopCriteriaStrategy = self.createStopCriteriaStrategy()
            
        stopCriteriaStrategy.setup(self)
        self.stopCriteriaStrategy = stopCriteriaStrategy
    
        if(initPositionGenerator is None):
            initPositionGenerator = self.createInitPositionGenerator()
            
        initPositionGenerator.setup(self)
        self.initPositionGenerator = initPositionGenerator
    
    
    def _configureLogging(self, filename, logLevel):
        logger = getLogger()
        logger.setLevel(logLevel)
        fh = logging.FileHandler(filename, "w")
        fh.setLevel(logLevel)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        logger.addHandler(fh)
        logger.addHandler(ch)
#         logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', 
#                             filename=filename, filemode='w', level=logLevel)
        
        
    def createStopCriteriaStrategy(self):
        """
        Returns a new instance of a stop criteria stategy
        """
        return IterationStopCriteriaStrategy()
    
    def createSampleFileUtil(self):
        """
        Returns a new instance of a File Util
        """
        return SampleFileUtil(self.filePrefix, reuseBurnin=self.reuseBurnin)
    
    def createInitPositionGenerator(self):
        """
        Returns a new instance of a Init Position Generator
        """
        return SampleBallPositionGenerator()
    
    @property
    def paramValues(self):
        return self.params[:,0]
    
    @property
    def paramWidths(self):
        return self.params[:,3]
    
    def startSampling(self):
        """
        Launches the sampling
        """
        try:
            if self.isMaster(): self.log(self.__str__())
            if(self.burninIterations>0):
                
                if(self.reuseBurnin):
                    pos, prob, rstate = self.loadBurnin()
                    datas = [None]*len(pos)
                    
                else:
                    pos, prob, rstate, datas = self.startSampleBurnin()
            else:
                pos = self.createInitPos()
                prob = None
                rstate = None
                datas = None
            # Starting from the final position in the burn-in chain, sample for 1000
            # steps.
            self.log("start sampling after burn in")
            start = time.time()
            self.sample(pos, prob, rstate, datas)
            end = time.time()
            self.log("sampling done! Took: " + str(round(end-start,4))+"s")
    
            # Print out the mean acceptance fraction. In general, acceptance_fraction
            # has an entry for each walker
            self.log("Mean acceptance fraction:"+ str(round(np.mean(self._sampler.acceptance_fraction), 4)))
        finally:
            if self._sampler.pool is not None:
                try:
                    self._sampler.pool.close()
                except AttributeError:
                    pass
                try:
                    self.storageUtil.close()
                except AttributeError:
                    pass



    def loadBurnin(self):
        """
        loads the burn in form the file system
        """
        self.log("reusing previous burn in")

        pos = self.storageUtil.importFromFile(self.filePrefix+c.BURNIN_SUFFIX)[-self.nwalkers:]

        prob = self.storageUtil.importFromFile(self.filePrefix+c.BURNIN_PROB_SUFFIX)[-self.nwalkers:]

        rstate= self.storageUtil.importRandomState(self.filePrefix+c.BURNIN_STATE_SUFFIX)

        self.log("loading done")
        return pos, prob, rstate
    
    
    def startSampleBurnin(self):
        """
        Runs the sampler for the burn in
        """
        self.log("start burn in")
        start = time.time()
        p0 = self.createInitPos()
        pos, prob, rstate, data = self.sampleBurnin(p0)
        end = time.time()
        self.log("burn in sampling done! Took: " + str(round(end-start,4))+"s")
        self.log("Mean acceptance fraction for burn in:" + str(round(np.mean(self._sampler.acceptance_fraction), 4)))
        
        self.resetSampler()
        
        return pos, prob, rstate, data
    
    
    def resetSampler(self):
        """
        Resets the emcee sampler in the master node
        """
        if self.isMaster():
            self.log("Reseting emcee sampler")
            # Reset the chain to remove the burn-in samples.
            self._sampler.reset()        
    
    
    
    def sampleBurnin(self, p0):
        """
        Run the emcee sampler for the burnin to create walker which are independent form their starting position
        """
        
        counter = 1
        for pos, prob, rstate, datas in self._sampler.sample(p0, iterations=self.burninIterations):
            if self.isMaster():
                self.storageUtil.persistBurninValues(pos, prob, datas)
                if(counter%10==0):
                    self.log("Iteration finished:" + str(counter))
                
            counter = counter + 1

        if self.isMaster():
            self.log("storing random state")
            self.storageUtil.storeRandomState(self.filePrefix+c.BURNIN_STATE_SUFFIX, rstate)
            
        return pos, prob, rstate, datas


    def sample(self, burninPos, burninProb=None, burninRstate=None, datas=None):
        """
        Starts the sampling process
        """
        counter = 1
        for pos, prob, _, datas in self._sampler.sample(burninPos, lnprob0=burninProb, rstate0=burninRstate, 
                                                        blobs0=datas, iterations=self.sampleIterations):
            if self.isMaster():
                self.log("Iteration done. Persisting", logging.DEBUG)
                self.storageUtil.persistSamplingValues(pos, prob, datas)
                
                if(self.stopCriteriaStrategy.hasFinished()):
                    break
                
                if(counter%10==0):
                    self.log("Iteration finished:" + str(counter))
                
            counter = counter + 1


    def isMaster(self):
        """
        Returns True. Can be overridden for multitasking i.e. with MPI
        """
        return True

    def log(self, message, level=logging.INFO):
        """
        Logs a message to the logfile
        """
        getLogger().log(level, message)
    
    
    def createEmceeSampler(self, callable, **kwargs):
        """
        Factory method to create the emcee sampler
        """
        if self.isMaster(): self.log("Using emcee "+str(emcee.__version__))
        return emcee.EnsembleSampler(self.nwalkers, 
                                     self.paramCount, 
                                     callable, 
                                     threads=self.threadCount, 
                                     **kwargs)

    def createInitPos(self):
        """
        Factory method to create initial positions
        """
        return self.initPositionGenerator.generate()


    def getChain(self):
        """
            Returns the sample chain
        """
        return self._sampler.chain
    
    def __str__(self, *args, **kwargs):
        """
            Returns the string representation of the sampler config
        """
        desc = "Sampler: " + str(type(self))+"\n" \
                "configuration: \n" \
                "  Params: " +str(self.paramValues)+"\n" \
                "  Burnin iterations: " +str(self.burninIterations)+"\n" \
                "  Samples iterations: " +str(self.sampleIterations)+"\n" \
                "  Walkers ratio: " +str(self.walkersRatio)+"\n" \
                "  Reusing burn in: " +str(self.reuseBurnin)+"\n" \
                "  init pos generator: " +str(self.initPositionGenerator)+"\n" \
                "  stop criteria: " +str(self.stopCriteriaStrategy)+"\n" \
                "  storage util: " +str(self.storageUtil)+"\n" \
                "likelihoodComputationChain: \n" + str(self.likelihoodComputationChain) \
                +"\n"
        
        return desc
