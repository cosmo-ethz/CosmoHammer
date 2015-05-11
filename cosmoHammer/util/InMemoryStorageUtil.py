
from copy import copy
import numpy as np

class InMemoryStorageUtil(object):
	"""
	Stores the data in memory
    
    :var samplesBurin: samples from the burn in
    :var probBurnin: likelihoods from the burn in
    :var samples: samples from the burn in
    :var prob: likelihoods from the burn in
	
	
	:param master: True if the sampler instance is the master
	
	"""
	
	def __init__(self, master=True):
		if(master):
			self.samplesBurnin = None
			self.probBurnin = None
			
			self.samples = None
			self.prob = None
	
	def importFromFile(self, filePath):
		print("InMemoryStorageUtil does not support importFromFile")
		return None

	def storeRandomState(self, filePath, randomState):
		print("InMemoryStorageUtil does not support storeRandomState")

	def importRandomState(self, filePath):
		print("InMemoryStorageUtil does not support importRandomState")
		return None

	def persistBurninValues(self, pos, prob, data):
		if(self.samplesBurnin is None):
			self.samplesBurnin = copy(pos)
		else:
			self.samplesBurnin = np.append(self.samplesBurnin, pos, axis=0)
		
		if(self.probBurnin is None):
			self.probBurnin = prob
		else:	
			self.probBurnin = np.append(self.probBurnin, prob, axis=0)

		
	def persistSamplingValues(self, pos, prob, data):
		if(self.samples is None):
			self.samples = copy(pos)
		else:
			self.samples = np.append(self.samples, pos, axis=0)
		
		if(self.prob is None):
			self.prob = prob
		else:	
			self.prob = np.append(self.prob, prob, axis=0)

	def __str__(self, *args, **kwargs):
		return "InMemoryStorageUtil"