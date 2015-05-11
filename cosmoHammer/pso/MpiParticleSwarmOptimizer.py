'''
Created on Oct 28, 2013

@author: J.Akeret
'''
from __future__ import print_function, division, absolute_import, \
    unicode_literals
    
import multiprocessing
import numpy

from cosmoHammer.util.MpiUtil import MpiPool, mpiBCast
from cosmoHammer.pso.ParticleSwarmOptimizer import ParticleSwarmOptimizer



class MpiParticleSwarmOptimizer(ParticleSwarmOptimizer):
    """
    PSO with support for MPI to distribute the workload over multiple nodes
    """
    
    def __init__(self, func, low, high, particleCount=25, threads=1):
        self.threads = threads
        pool = MpiPool(self._getMapFunction())
        super(MpiParticleSwarmOptimizer, self).__init__(func, low, high, particleCount=particleCount, pool=pool)
        
        
    def _getMapFunction(self):
        if self.threads > 1:
            pool = multiprocessing.Pool(self.threads)
            return pool.map
        else:
            return map

    def _converged(self, it, p, m, n):
        
        if(self.isMaster()):
            converged =  super(MpiParticleSwarmOptimizer, self)._converged(it, p, m, n)
        else:
            converged = False
        
        converged = mpiBCast(converged)
        return converged
    
    def _get_fitness(self,swarm):
        mapFunction = self.pool.map
        
        mpiSwarm = mpiBCast(swarm)
        
        pos = numpy.array([part.position for part in mpiSwarm])
        results =  mapFunction(self.func, pos)
        lnprob = numpy.array([l[0] for l in results])
        for i, particle in enumerate(swarm):
            particle.fitness = lnprob[i]
            particle.position = pos[i]
    
    def isMaster(self):
        return self.pool.isMaster()