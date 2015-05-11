.. _install:

Installation
============

Since ``CosmoHammer`` is a pure Python module, it should be pretty easy to install.

At the command line via pip::

    $ pip install cosmohammer

This will install the package and all of the required dependencies. 

.. note:: If you wish to use `CosmoHammer` on a cluster with MPI you need to manually install `mpi4py <https://pypi.python.org/pypi/mpi4py>`_. 

From source
-----------

Once you've downloaded and unpacked the source, you can navigate into the
root source directory and run:

::

    $ python setup.py build
    $ python setup.py install --user



You might need to run this using ``sudo`` depending on your Python
installation.

Cosmological parameters from CMB data
------------------------------------------------------------------------

To estimate cosmological parameters you will need likelihood and core modules for CosmoHammer.
See the cosmoHammerPlugins project `GitHub <https://github.com/cosmo-ethz/CosmoHammerPlugins>`_ for the modules publicly available at the moment.
