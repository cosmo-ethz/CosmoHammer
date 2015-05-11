
import multiprocessing
from cosmoHammer.MpiCosmoHammerSampler import MpiCosmoHammerSampler


class ConcurrentMpiCosmoHammerSampler(MpiCosmoHammerSampler):
    """
    A sampler implementation extending the mpi sampler in order to allow to 
    distribute the computation with MPI and using multiprocessing on a single node.

    :param threads:  (optional)
        The number of threads to use for parallelization. If ``threads == 1``,
        then the ``multiprocessing`` module is not used but if
        ``threads > 1``, then a ``Pool`` object is created
        
    :param kwargs: key word arguments passed to the CosmoHammerSampler

    """
    def __init__(self, threads=1, **kwargs):
        """
        CosmoHammer sampler implementation
        
        """
        
        self.threads = threads
        
        super(ConcurrentMpiCosmoHammerSampler, self).__init__(**kwargs)
        
        
    def _getMapFunction(self):
        if self.threads > 1:
            pool = multiprocessing.Pool(self.threads)
            return pool.map
        else:
            return map
