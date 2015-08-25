
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
    def get_instance(self):
        """
            Returns the singleton instance of the database.
            NOT RECOMMENDED. It allows specific supplier DB operations.
            * Returns current specific DB controller. None if there is any problem creating it.           
        """
        pass
        
        
    # CRUD METHODS
    
    @abstractmethod 
    def get_all_data(self):
        """
            Get all data from DB. IT SHOULD BE FIXED.
        """
        pass
    
    @abstractmethod 
    def get_data_by(self, condition):
        """
            Get data from DB with some condition.
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
        