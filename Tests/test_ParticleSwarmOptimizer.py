"""
Test the CosmoHammerSampler module.

Execute with py.test -v

"""
import numpy as np

from cosmoHammer.ChainContext import ChainContext
from cosmoHammer.pso.ParticleSwarmOptimizer import ParticleSwarmOptimizer
from cosmoHammer.pso.ParticleSwarmOptimizer import Particle

class TestCosmoHammerSampler(object):
    ctx = None
    params = np.array([[1,2,3],[4,5,6]])
    
    def setup(self):
        self.ctx=ChainContext(self, self.params)
        
    def test_Particle(self):
        particle = Particle.create(2)
        assert particle.fitness == -np.inf
        
        assert particle == particle.pbest
        
        particle2 = particle.copy()
        assert particle.fitness == particle2.fitness
        assert particle.paramCount == particle2.paramCount
        assert (particle.position == particle2.position).all()
        assert (particle.velocity == particle2.velocity).all()
        
        
        particle.fitness = 1
        particle.updatePBest()
        
        assert particle.pbest.fitness == 1        
    

    def test_setup(self):
        low = np.zeros(2)
        high = np.ones(2)
        pso = ParticleSwarmOptimizer(None, low, high, 10)
        
        assert pso.swarm is not None
        assert len(pso.swarm) == 10
        
        position = [part.position for part in pso.swarm]
        
        assert (position>=low).all()
        assert (position<=high).all()
        
        velocity = [part.velocity for part in pso.swarm]
        assert (velocity == np.zeros(2)).all()
        
        fitness = [part.fitness == 0 for part in pso.swarm]
        assert all(fitness)
        
        assert pso.gbest.fitness == -np.inf
        
        
    def test_optimize(self):
        low = np.zeros(2)
        high = np.ones(2)
        func = lambda p: (-np.random.rand(), None)
        pso = ParticleSwarmOptimizer(func, low, high, 10)
        
        maxIter=10
        swarms, gbests = pso.optimize(maxIter)
        assert swarms is not None
        assert gbests is not None
        assert len(swarms) == maxIter
        assert len(gbests) == maxIter
        
        fitness = [part.fitness != 0 for part in pso.swarm]
        assert all(fitness)
        
        assert pso.gbest.fitness != -np.inf 
        
        