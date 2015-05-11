=======================================================
Cosmological parameter estimation with the MCMC Hammer
=======================================================

.. image:: https://badge.fury.io/py/cosmoHammer.png
    :target: http://badge.fury.io/py/cosmoHammer

.. image:: https://travis-ci.org/cosmo-ethz/CosmoHammer.png?branch=master
        :target: https://travis-ci.org/cosmo-ethz/CosmoHammer
        
.. image:: https://coveralls.io/repos/cosmo-ethz/CosmoHammer/badge.svg
  		:target: https://coveralls.io/r/cosmo-ethz/CosmoHammer

.. image:: http://img.shields.io/badge/arXiv-1212.1721-orange.svg?style=flat
        :target: http://arxiv.org/abs/1212.1721



CosmoHammer is a framework which embeds `emcee <http://arxiv.org/abs/1202.3665>`_ , an implementation by Foreman-Mackey et al. (2012) of the `Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler <http://msp.berkeley.edu/camcos/2010/5-1/p04.xhtml>`_ by Goodman and Weare (2010).

It gives the user the possibility to plug in modules for the computation of any desired likelihood. The major goal of the software is to reduce the complexity when one wants to extend or replace the existing computation by modules which fit the user's needs as well as to provide the possibility to easily use large scale computing environments. 

We published a `paper <http://arxiv.org/abs/1212.1721>`_ in the `Astronomy and Computing Journal <http://authors.elsevier.com/sd/article/S221313371300022X>`_ which discusses the advantages and performance of our framework.

This project has been realized in collaboration with the `Institute of 4D Technologies <http://www.fhnw.ch/engineering/i4ds/homepage>`_ of the `University of Applied Sciences and Arts Northwest Switzerland <http://www.fhnw.ch/homepage>`_ (Fachhochschule Nordwestschweiz - FHNW).

The development is coordinated on `GitHub <http://github.com/cosmo-ethz/CosmoHammer>`_ and contributions are welcome. The documentation of **CosmoHammer** is available at `readthedocs.org <http://cosmohammer.readthedocs.org/>`_ and the package is distributed over `PyPI <https://pypi.python.org/pypi/CosmoHammer>`_.

For all public modules such as PyCamb, WMAP, Planck and more, see the cosmoHammerPlugins project at http://github.com/cosmo-ethz/CosmoHammerPlugins.

