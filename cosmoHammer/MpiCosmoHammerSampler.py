
from cosmoHammer import CosmoHammerSampler

from cosmoHammer.util.SampleFileUtil import SampleFileUtil
from cosmoHammer.util.MpiUtil import MpiPool, mpiBCast

class MpiCosmoHammerSampler(CosmoHammerSampler):
    """
    A sampler implementation extending the regular sampler in order to allow for distributing 
    the computation with MPI.

    :param kwargs:  
        key word arguments passed to the CosmoHammerSampler
    
    """
    def __init__(self, **kwargs):
        """
        CosmoHammer sampler implementation
        
        """
        self.pool = MpiPool(self._getMapFunction())
        self.rank = self.pool.rank
        
        super(MpiCosmoHammerSampler, self).__init__(pool=self.pool, **kwargs)
        
        
        
    def _getMapFunction(self):
        """
        Returns the build in map function
        """
        return map
    
    def createSampleFileUtil(self):
        """
        Returns a new instance of a File Util
        """
        return SampleFileUtil(self.filePrefix, self.isMaster(), reuseBurnin=self.reuseBurnin)
    
       
    def sampleBurnin(self, p0):
        """
        Starts the sampling process. The master node (mpi rank = 0) persists the result to the disk
        """
        p0 = mpiBCast(p0)
        
        self.log("MPI Process rank "+ str(self.rank)+" starts sampling")
        return super(MpiCosmoHammerSampler, self).sampleBurnin(p0);
   
    def sample(self, burninPos, burninProb, burninRstate, datas):
        """
        Starts the sampling process. The master node (mpi rank = 0) persists the result to the disk
        """
        burninPos = mpiBCast(burninPos)
        burninProb = mpiBCast(burninProb)
        burninRstate = mpiBCast(burninRstate)
        
        self.log("MPI Process rank "+ str(self.rank)+" starts sampling")
        super(MpiCosmoHammerSampler, self).sample(burninPos, burninProb, burninRstate, datas);

            
    def loadBurnin(self):
        """
        loads the burn in form the file system
        """
        if(self.isMaster()):
            pos, prob, rstate = super(MpiCosmoHammerSampler, self).loadBurnin()
        else:
            pos, prob, rstate = []
            
        pos = mpiBCast(pos)
        prob = mpiBCast(prob)
        rstate = mpiBCast(rstate)
        
        self.log("loading done")
        return pos, prob, rstate
    
    def createInitPos(self):
        """
        Factory method to create initial positions
        """   
        #bcast the positions to ensure that all mpi nodes start at the same position
        return mpiBCast(super(MpiCosmoHammerSampler, self).createInitPos())


    def isMaster(self):
        """
        Returns true if the rank is 0
        """
        return self.pool.isMaster()