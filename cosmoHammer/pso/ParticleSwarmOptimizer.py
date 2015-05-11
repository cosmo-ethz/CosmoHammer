'''
Created on Sep 30, 2013

@author: J. Akeret
'''
from __future__ import print_function, division, absolute_import, unicode_literals
from copy import copy
from math import floor
import math
import multiprocessing
import numpy

class ParticleSwarmOptimizer(object):
    '''
    Optimizer using a swarm of particles
    
    :param func:
        A function that takes a vector in the parameter space as input and
        returns the natural logarithm of the posterior probability for that
        position.

    :param low: array of the lower bound of the parameter space
    :param high: array of the upper bound of the parameter space
    :param particleCount: the number of particles to use. 
    :param threads: (optional)
        The number of threads to use for parallelization. If ``threads == 1``,
        then the ``multiprocessing`` module is not used but if
        ``threads > 1``, then a ``Pool`` object is created and calls to
        ``lnpostfn`` are run in parallel.

    :param pool: (optional)
        An alternative method of using the parallelized algorithm. If
        provided, the value of ``threads`` is ignored and the
        object provided by ``pool`` is used for all parallelization. It
        can be any object with a ``map`` method that follows the same
        calling sequence as the built-in ``map`` function.
    
    '''


    def __init__(self, func, low, high, particleCount=25, threads=1, pool=None):
        '''
        Constructor
        '''
        self.func = func
        self.low = low
        self.high = high
        self.particleCount = particleCount
        self.threads = threads
        self.pool = pool
        
        if self.threads > 1 and self.pool is None:
            self.pool = multiprocessing.Pool(self.threads)
        
        self.paramCount = len(self.low)
        
        self.swarm = self._initSwarm()
        self.gbest = Particle.create(self.paramCount)
        
    def _initSwarm(self):
        swarm = []
        for _ in range(self.particleCount):
            swarm.append(Particle(numpy.random.uniform(self.low, self.high, size=self.paramCount), numpy.zeros(self.paramCount)))
        
        return swarm
        
    def sample(self, maxIter=1000, c1=1.193, c2=1.193, p=0.7, m=10**-3, n=10**-2):
        """
        Launches the PSO. Yields the complete swarm per iteration
        
        :param maxIter: maximum iterations
        :param c1: cognitive weight
        :param c2: social weight
        :param p: stop criterion, percentage of particles to use 
        :param m: stop criterion, difference between mean fitness and global best
        :param n: stop criterion, difference between norm of the particle vector and norm of the global best
        """
        self._get_fitness(self.swarm)
        i = 0
        while True:
            
            
            for particle in self.swarm:
                if ((self.gbest.fitness)<particle.fitness):
                    
                    self.gbest = particle.copy()
                    #if(self.isMaster()):
                        #print("new global best found %i %s"%(i, self.gbest.__str__()))
                    
                if (particle.fitness > particle.pbest.fitness):
                    particle.updatePBest()

            if(i>=maxIter):
                print("max iteration reached! stoping")
                return
            
            if(self._converged(i, p=p,m=m, n=n)):
                if(self.isMaster()):
                    print("converged after %s iterations!"%i)
                    print("best fit found: ", self.gbest.fitness, self.gbest.position)
                return

            
            for particle in self.swarm:
                 
                w = 0.5 + numpy.random.uniform(0,1,size=self.paramCount)/2
                #w=0.72
                part_vel = w * particle.velocity
                cog_vel = c1 * numpy.random.uniform(0,1,size=self.paramCount) * (particle.pbest.position - particle.position)
                soc_vel = c2 * numpy.random.uniform(0,1,size=self.paramCount) * (self.gbest.position - particle.position)
                particle.velocity = part_vel + cog_vel + soc_vel
                particle.position = particle.position + particle.velocity
            
            self._get_fitness(self.swarm)

            swarm = []
            for particle in self.swarm:
                swarm.append(particle.copy()) 
            yield swarm
            
            i+=1
        
    def optimize(self, maxIter=1000, c1=1.193, c2=1.193, p=0.7, m=10**-3, n=10**-2):
        """
        Runs the complete optimiziation.
        
        :param maxIter: maximum iterations
        :param c1: cognitive weight
        :param c2: social weight
        :param p: stop criterion, percentage of particles to use 
        :param m: stop criterion, difference between mean fitness and global best
        :param n: stop criterion, difference between norm of the particle vector and norm of the global best

        :return swarms, gBests: the swarms and the global bests of all iterations
        """
        
        swarms = []
        gBests = []
        for swarm in self.sample(maxIter,c1,c2,p,m,n):
            swarms.append(swarm)
            gBests.append(self.gbest.copy())
        
        return swarms, gBests
        
    def _get_fitness(self,swarm):
        
        # If the `pool` property of the pso has been set (i.e. we want
        # to use `multiprocessing`), use the `pool`'s map method. Otherwise,
        # just use the built-in `map` function.
        if self.pool is not None:
            mapFunction = self.pool.map
        else:
            mapFunction = map
        
        pos = numpy.array([part.position for part in swarm])
        results =  mapFunction(self.func, pos)
        lnprob = numpy.array([l[0] for l in results])
        for i, particle in enumerate(swarm):
            particle.fitness = lnprob[i]

    def _converged(self, it, p, m, n):
#        test = self._convergedSpace2(p=p)
#        print(test)
        fit = self._convergedFit(it=it, p=p, m=m)
        if(fit):
            space = self._convergedSpace(it=it, p=p, m=n)
            return space
        else:
            return False
        
    def _convergedFit(self, it, p, m):
        bestSort = numpy.sort([particle.pbest.fitness for particle in self.swarm])[::-1]
        meanFit = numpy.mean(bestSort[1:math.floor(self.particleCount*p)])
#        print( "best %f, meanFit %f, ration %f"%( self.gbest[0], meanFit, abs((self.gbest[0]-meanFit))))
        return (abs(self.gbest.fitness-meanFit)<m)
    
    def _convergedSpace(self, it, p, m):
        sortedSwarm = [particle for particle in self.swarm]
        sortedSwarm.sort(key=lambda part: -part.fitness)
        bestOfBest = sortedSwarm[0:int(floor(self.particleCount*p))]
        
        diffs = []
        for particle in bestOfBest:
            diffs.append(self.gbest.position-particle.position)
            
        maxNorm = max(list(map(numpy.linalg.norm, diffs)))
        return (abs(maxNorm)<m)

    def _convergedSpace2(self, p):
        #Andres N. Ruiz et al.
        sortedSwarm = [particle for particle in self.swarm]
        sortedSwarm.sort(key=lambda part: -part.fitness)
        bestOfBest = sortedSwarm[0:int(floor(self.particleCount*p))]
        
        positions = [particle.position for particle in bestOfBest]
        means = numpy.mean(positions, axis=0)
        delta = numpy.mean((means-self.gbest.position)/self.gbest.position)
        return numpy.log10(delta) < -3.0


    def isMaster(self):
        return True   

class Particle(object):
    """
    Implementation of a single particle
    
    :param position: the position of the particle in the parameter space
    :param velocity: the velocity of the particle
    :param fitness: the current fitness of the particle
    
    """
    
    
    def __init__(self, position, velocity, fitness = 0):
        self.position = position
        self.velocity = velocity
        
        self.fitness = fitness
        self.paramCount = len(self.position)
        self.pbest = self

    @classmethod
    def create(cls, paramCount):
        """
        Creates a new particle without position, velocity and -inf as fitness
        """
        
        return Particle(numpy.array([[]]*paramCount),
                 numpy.array([[]]*paramCount),
                 -numpy.Inf)
        
    def updatePBest(self):
        """
        Sets the current particle representation as personal best
        """
        self.pbest = self.copy()
        
    def copy(self):
        """
        Creates a copy of itself
        """
        return Particle(copy(self.position),
                        copy(self.velocity),
                        self.fitness)
        
    def __str__(self):
        return "%f, pos: %s velo: %s"%(self.fitness, self.position, self.velocity)
    
    def __unicode__(self):
        return self.__str__()