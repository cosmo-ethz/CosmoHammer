import itertools
import os
from cosmoHammer import getLogger
import time

# If mpi4py is installed, import it.
try:
    from mpi4py import MPI
    MPI = MPI
except ImportError:
    MPI = None

class MpiPool(object):
    """
    Implementation of a mpi based pool. Currently it supports only the map function.
    
    :param mapFunction: the map function to apply on the mpi nodes
    
    """
    def __init__(self, mapFunction):
        self.rank = MPI.COMM_WORLD.Get_rank()
        self.mapFunction = mapFunction
    
    def map(self, function, sequence):
        """
        Emulates a pool map function using Mpi.
        Retrieves the number of mpi processes and splits the sequence of walker position 
        in order to allow each process its block
        
        :param function: the function to apply on the items of the sequence
        :param sequence: a sequence of items
        
        :returns sequence: sequence of results
        """
        
        (rank,size) = (MPI.COMM_WORLD.Get_rank(),MPI.COMM_WORLD.Get_size())
        #sync
        sequence = mpiBCast(sequence)
        
        getLogger().debug("Rank: %s, pid: %s MpiPool: starts processing iteration" %(rank, os.getpid()))
        #split, process and merge the sequence
        mergedList = mergeList(MPI.COMM_WORLD.allgather(
                                                  self.mapFunction(function, splitList(sequence,size)[rank])))
        getLogger().debug("Rank: %s, pid: %s MpiPool: done processing iteration"%(rank, os.getpid()))
#         time.sleep(10)
        return mergedList
    
    def isMaster(self):
        """
        Returns true if the rank is 0
        """
        return (self.rank==0)
    
def mpiBCast(value):
    """
    Mpi bcasts the value and Returns the value from the master (rank = 0).
    """
    getLogger().debug("Rank: %s, pid: %s MpiPool: bcast", MPI.COMM_WORLD.Get_rank(), os.getpid())
    return MPI.COMM_WORLD.bcast(value)

def splitList(list, n):
    """
    Splits the list into block of equal sizes (listlength/n)
    
    :param list: a sequence of items
    :param n: the number of blocks to create
    
    :returns sequence: a list of blocks
    """
    getLogger().debug("Rank: %s, pid: %s MpiPool: splitList", MPI.COMM_WORLD.Get_rank(), os.getpid())
    blockLen = len(list) / float(n)
    return [list[int(round(blockLen * i)): int(round(blockLen * (i + 1)))] for i in range(n)]    

def mergeList(lists):
    """
    Merges the lists into one single list
    
    :param lists: a list of lists
    
    :returns list: the merged list
    """
    getLogger().debug("Rank: %s, pid: %s MpiPool: mergeList", MPI.COMM_WORLD.Get_rank(), os.getpid())
    return list(itertools.chain(*lists))



