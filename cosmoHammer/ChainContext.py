
PARENT_KEY = "key_parent"
PARAMS_KEY = "key_params"
DATA_KEY = "key_data"

class ChainContext(object):
    """
    Context holding a dict to store data and information durring the computation of the likelihood
    """
    
    def __init__(self, parent, params):
        """
        Constructor of the context
        """
        
        self._data = dict()
        self.add(PARENT_KEY, parent)
        self.add(PARAMS_KEY, params)
        self.add(DATA_KEY, dict())
        
    def add(self, key, value):
        """
        Adds the value to the context using the key
        
        :param key: string
            key to use
        :param value: object
            the value to store
            
        """
        self._data[key] = value
        
    def remove(self, key):
        """
        Removes the value from the context
        
        :param key: string
            key to remove from the context
        """
        assert key != None
        del(self._data[key])
        
    def contains(self, key):
        """
        Checks if the key is in the context
        
        :param key: string
            key to check
            
        :return: True if the key is in the context
        """
        return key in self._data
    
    def get(self, key, default=None):
        """
        Returns the value stored in the context at the key or the default value in the 
        context doesn't contain the key
        
        :param key: string
            key to use
        :param default: string
            the default value to use if the key is not available
        """
        if(self.contains(key)):
            return self._data[key]
        
        return default
        
    def getParams(self):
        """
        Returns the currently processed parameters
        
        :return: The param of this context
        """
        return self.get(PARAMS_KEY)
    
    def getParent(self):
        """
        Returns the parent
        
        :return: The parent chain of this context
        """
        return self.get(PARENT_KEY)
    
    def getData(self):
        """
        Returns the data
        
        :return: The data of this context
        """
        return self.get(DATA_KEY)
        