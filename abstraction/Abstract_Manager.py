
from abc import ABCMeta, abstractmethod

"""
    Abstract class that must be implemented by all specific DataBase managers to support its interface.
"""
class AbstractManager(object):
    
    __metaclass__ = ABCMeta

    @abstractmethod    
    def __init__(self): pass
    
    
    @abstractmethod    
    def __str__(self): pass
       
           
    @abstractmethod 
    def _get_instance(self):
        """
            Returns the singleton instance of specific DB.
            NOT RECOMMENDED: It allows specific DB provider operations, to use in very specific situations.
            You should use normal CRUD functionality available in this class instead. 
            * Returns current specific DB instance. None if there is any problem creating it.           
        """
        pass
        
        
    # CRUD METHODS
    
    @abstractmethod 
    def get_all_data(self):
        """
            Get all data from DB.
        """
        pass
    
    @abstractmethod 
    def _get_data_by(self, condition):
        """
            Get data from DB with some free condition.
            NOT RECOMMENDED. It allows specific supplier DB operations.
        """
        pass
    
            
    @abstractmethod 
    def delete_all_data(self):
        """
            Delete all the data from DB
        """
        pass
          
    @abstractmethod 
    def insert_data(self, var):
        """
            Adds to our database all variables passed as arguments
            * var {list} 
        """
        pass
        