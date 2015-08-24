
from abc import ABCMeta, abstractmethod

"""
    Abstract class that must be implemented by all specific DataBase managers to support its interface.
"""
class AbstractManager(object):
    
    __metaclass__ = ABCMeta

    @abstractmethod    
    def __str__(self): pass
       
           
    @abstractmethod 
    def get_instance():
        """
            Returns the singleton instance of the database.
            NOT RECOMMENDED. It allows specific supplier DB operations.
            * Returns current specific DB controller. None if there is any problem creating it.           
        """
        pass
        
        
    # CRUD METHODS
    
    @abstractmethod 
    def get_all_data():
        """
            Get all data from DB. It should be improved.
        """
        pass
            
    @abstractmethod 
    def delete_all_data():
        """
            Delete all the data from DB
        """
        pass
          
    @abstractmethod 
    def insert_data(var):
        """
            Adds to our database all variables passed as arguments
            * var {list} 
        """
        pass
        