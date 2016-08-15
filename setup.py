#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from setuptools import find_packages

try:
    from setuptools import setup, Extension
    setup, Extension
except ImportError:
    from distutils.core import setup, Extension
    setup, Extension

from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


desc = open("README.rst").read()
required = ["numpy", "emcee"]
test_requires = ["mock"]

PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

setup(
    name="cosmoHammer",
    version='0.6.0',
    author='Joel Akeret',
    author_email="jakeret@phys.ethz.ch",
    url="http://www.cosmology.ethz.ch/research/software-lab/cosmohammer.html",
    license="GPLv3",
    packages=find_packages(PACKAGE_PATH, "Tests"),
    description="Cosmological parameter estimation with the MCMC Hammer",
    long_description=desc,
    install_requires=required,
    test_requires=test_requires,
    package_data={"": ["LICENSE"],
                  'cosmoHammer': ['data/*.dat']},
    include_package_data=True,
    keywords=["CosmoHammer",
              "parameter estimation", 
              "cosmology", 
              "MCMC"],
    cmdclass = {'test': PyTest},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
