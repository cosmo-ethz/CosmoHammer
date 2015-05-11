'''
Created on Oct 30, 2013

@author: J.Akeret
'''
from __future__ import print_function, division, absolute_import, \
    unicode_literals

from numpy.linalg.linalg import norm
from scipy.optimize.minpack import leastsq
from scipy.optimize import minimize
import numpy
import sys

def parabola(p, x):
    """
    Computation of the paraboloid for the given curvature matrix and samples.
    :param x: vector containing the lower triangle of the matrix and the offset from the true mean
    :param p: list of samples
    
    :return: vector y from f(x,p)
    """
    
    theta = x
    leng, dim = theta.shape
    R, mu = transform(dim, p)
    
    v = numpy.zeros(leng)
#     theta += numpy.outer(mu, numpy.ones(len(theta))).T
    for i,thetaj in enumerate(theta):
#         v[i] = numpy.dot(thetaj.T,numpy.dot(R, thetaj)) + 2 * numpy.dot(thetaj, numpy.dot(R, mu))
        v[i] = numpy.dot(thetaj.T,numpy.dot(R, thetaj)) + numpy.dot(thetaj,  mu)

    return numpy.array(v)


def errfunc(p,theta,delta):
    """
    Error function defined by f(theta) - delta
    :param p: list of samples
    :param theta: the curvature matrix. see parabola def
    :param delta: the measured values
    """
    return parabola(p, theta) - delta

def transform(dim, p):
    """
    Transforms a vector containg the lower triangle of a matrix into a symmetric matrix
    
    :param p: the vector
    
    :return: the matrix and left over values
    """
    R = numpy.zeros((dim,dim))
    k=0
    for i in range(dim):
        for j in range(0,i+1):
            R[i,j]= p[k]
            k +=1
            
    R += R.T - numpy.diag(R.diagonal())
    
    xbar = p[k:]

    return R, xbar

def reverse(dim, R):
    """
    Transforms a symmetric matrix into a vector containig the lower triangle
    
    :param R: the symmetric matrix
    
    :return: the vector
    """
    p = numpy.zeros(dim*(dim+1)/2)
    k=0
    for i in range(dim):
        for j in range(0,i+1):
            p[k] = R[i,j]
            k +=1
            
    return p    


class ParaboloidFitter(object):
    '''
    Fits a paraboloid centered around the global best fit of the PSO by estimating a curvarture
    matrix with the particle given in the swarm
    
    :param swarm: list of particles
    :param gbest: the global best particle at the last iteration
    '''


    def __init__(self, swarm, gbest):
        '''
        Constructor
        '''
        self.swarm = swarm
        self.gbest = gbest
        
    def fit(self):
        """
        Fits the paraboloid to the swarm particles
        
        :return: the mean = global best position and the estimated covariance matrix
        """
        
        scale = 10**0
        dim = len(self.gbest.position) 
        
        x = numpy.array([particle.position * scale for particle in self.swarm])
        theta = (x - self.gbest.position * scale) / (self.gbest.position * scale)
        norms = numpy.array(list(map(norm, theta)))
        #print(Counter(b))
        b = (norms < 0.1)
        theta = theta[b]
        fitness = numpy.array([particle.fitness * scale for particle in self.swarm])

#         b = numpy.logical_and((norms < 0.1), fitness != -numpy.inf)
        fitness =  fitness[b]
        delta = -2*(fitness - self.gbest.fitness * scale)
        
        p0 = numpy.zeros(dim*(dim+1)/2 + dim)
        popt, _cov,infodict,mesg,ier = leastsq(errfunc, p0, args=(theta,delta),full_output=True)
        print(mesg)
         
         
        ss_err=(infodict['fvec']**2).sum()
        ss_tot=((delta-delta.mean())**2).sum()
        rsquared=1-(ss_err/ss_tot)
        print("rsquared", rsquared)
        R, mu = transform(dim, popt)
        print(mu)
#         print("found R:\n", R)
        _cov = rescale(R, self.gbest.position, dim)
        print("found _cov:\n", _cov)
        
#         cons = (
#          {'type': 'ineq',
#           'fun' : lambda x: bound(x)})
#           
#         res = minimize(errfunc2, p0, args=(theta, delta), constraints=cons, method='SLSQP', options={'disp': True, "ftol":10**-10})
#         popt=res.x
#         R, mu = transform(dim, popt)
#         print(mu)
# #         print("found R:\n", R)
#         _cov = rescale(R, self.gbest.position, dim)
#         print("found _cov:\n", _cov)

#         eigen = numpy.linalg.eigvals(R)
#         print("-->eigen:", min(eigen), max(eigen), min(eigen)/max(eigen))
#         R2 = numpy.empty((dim, dim))
#         for i in range(dim):
#             for j in range(dim):
#                 R2[i,j] = R[i,j]/self.gbest.position[i]/self.gbest.position[j]
#         
#         print("R\n", R2)
        
#         _cov = rescale(R, self.gbest.position, dim)
#         print("found _cov:\n", _cov)
#         print("=> _cov diag", cov2.diagonal())
#         sigma = numpy.sqrt(numpy.diag(cov2))
#         print( "=> found sigma:", sigma)

        return self.gbest.position, _cov

def rescale(R, v, dim):
        _cov = numpy.linalg.inv(R)
        #rescaling
        cov2 = numpy.empty((dim, dim))
        for i in range(dim):
            for j in range(dim):
                cov2[i,j] = _cov[i,j] * v[i] * v[j]
        return cov2