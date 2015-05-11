
import pickle
import numpy as np
import cosmoHammer.Constants as c

class SampleFileUtil(object):
	"""
	Util for handling sample files
	
	:param filePrefix: the prefix to use
	:param master: True if the sampler instance is the master
	:param  reuseBurnin: True if the burn in data from a previous run should be used
	
	"""
	
	def __init__(self, filePrefix, master=True, reuseBurnin=False):
		self.filePrefix = filePrefix
		
		if(master):
			if(reuseBurnin):
				mode = "r"
			else:
				mode = "w"
			self.samplesFileBurnin = open(self.filePrefix+c.BURNIN_SUFFIX, mode)
			self.probFileBurnin = open(self.filePrefix+c.BURNIN_PROB_SUFFIX, mode)
			
			self.samplesFile = open(self.filePrefix+c.FILE_SUFFIX, "w")
			self.probFile = open(self.filePrefix+c.PROB_SUFFIX, "w")
	
	def importFromFile(self, filePath):
		values = np.loadtxt(filePath, dtype=float)
		return values

	def storeRandomState(self, filePath, randomState):
		with open(filePath,'wb') as f:
			pickle.dump(randomState, f)

	def importRandomState(self, filePath):
		with open(filePath,'rb') as f:
			state = pickle.load(f)
		return state

	def persistBurninValues(self, pos, prob, data):
		self.persistValues(self.samplesFileBurnin, self.probFileBurnin, pos, prob, data)
		
	def persistSamplingValues(self, pos, prob, data):
		self.persistValues(self.samplesFile, self.probFile, pos, prob, data)
		

	def persistValues(self, posFile, probFile, pos, prob, data):
		"""
		Writes the walker positions and the likelihood to the disk
		"""
		posFile.write("\n".join(["\t".join([str(q) for q in p]) for p in pos]))
		posFile.write("\n")
		posFile.flush()
		
		probFile.write("\n".join([str(p) for p in prob]))
		probFile.write("\n")
		probFile.flush();
		
	def close(self):
		self.samplesFileBurnin.close()
		self.probFileBurnin.close()
		self.samplesFile.close()
		self.probFile.close()

	def __str__(self, *args, **kwargs):
		return "SampleFileUtil"