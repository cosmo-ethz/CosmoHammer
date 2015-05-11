"""
Test the TestSampleFileUtil module.

Execute with py.test -v

"""
from __future__ import print_function, division, absolute_import, unicode_literals

import tempfile
import os
import numpy

import cosmoHammer.Constants as c
from cosmoHammer.util.SampleFileUtil import SampleFileUtil

class TestSampleFileUtil(object):

    prefix = "test"
    
    def createFileUtil(self):
        tempPath = tempfile.mkdtemp()
        tempPath = os.path.join(tempPath, self.prefix)
        fileUtil = SampleFileUtil(tempPath, True)
        return fileUtil, tempPath
    
    def test_not_master(self):
        tempPath = tempfile.mkdtemp()
        SampleFileUtil(tempPath, False)
        fileList = os.listdir(tempPath)
        assert len(fileList) == 0
        
        
    def test_persistBurninValues(self):
        fileUtil, tempPath = self.createFileUtil()
        
        pos = numpy.ones((10,5))
        prob = numpy.zeros(10)
        
        fileUtil.persistBurninValues(pos, prob, None)
        
        cPos = numpy.loadtxt(tempPath + c.BURNIN_SUFFIX)
        cProb = numpy.loadtxt(tempPath + c.BURNIN_PROB_SUFFIX)
        
        assert (pos == cPos).all()
        assert (prob == cProb).all()
        
        
    def test_persistSamplingValues(self):
        fileUtil, tempPath = self.createFileUtil()
        
        pos = numpy.ones((10,5))
        prob = numpy.zeros(10)
        
        fileUtil.persistSamplingValues(pos, prob, None)
        
        cPos = numpy.loadtxt(tempPath + c.FILE_SUFFIX)
        cProb = numpy.loadtxt(tempPath + c.PROB_SUFFIX)
        
        assert (pos == cPos).all()
        assert (prob == cProb).all()
        
    def test_importFromFile(self):
        fileUtil, tempPath = self.createFileUtil()
        
        pos = numpy.ones((10,5))
        prob = numpy.zeros(10)
        
        fileUtil.persistSamplingValues(pos, prob, None)
        
        cPos = fileUtil.importFromFile(tempPath + c.FILE_SUFFIX)
        cProb = fileUtil.importFromFile(tempPath + c.PROB_SUFFIX)
        
        assert (pos == cPos).all()
        assert (prob == cProb).all()
        
    def test_storeRandomState(self):
        fileUtil, tempPath = self.createFileUtil()
        
        rstate = numpy.random.mtrand.RandomState()
        fileUtil.storeRandomState(tempPath+c.BURNIN_STATE_SUFFIX, rstate)
        
        cRstate = fileUtil.importRandomState(tempPath+c.BURNIN_STATE_SUFFIX)
        
        print(rstate.get_state())
        oState = rstate.get_state()
        nState = cRstate.get_state()
        
        assert oState[0] == nState[0]
        assert all(oState[1] == nState[1])
        assert oState[2] == nState[2]
        assert oState[3] == nState[3]
        assert oState[4] == nState[4]
        