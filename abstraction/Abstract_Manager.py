
from abc import ABCMeta, abstractmethod

"""
    Abstract class that must be implemented by all specific DataBase managers to support its interface.
"""
class AbstractManager(object):
    
    __metaclass__ = ABCMeta
    
    OPERATORS = 'EQ','NO','AND','OR'
    SORTING = 'DESC','ASC'
    
    
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
    def get_data_by_conditions(self, conditions):
        """
            Makes a Request to the DB manager with a list of conditions.
            Returns an unsorted and limited amount of results defined by the specific DB manager.
                * conditions {list} conditions to all results to be obtained
                * {list} Return results.
        """
        pass
    
    @abstractmethod 
    def get_data_by_conditions_sorting(self, conditions, sorting_rules):
        """
            Makes a Request to the DB manager with a list of conditions and sorting rules.
            Returns a limited amount of results defined by the specific DB manager.
                * conditions {list} conditions to all results to be obtained
                * sorting_rules {list} stantard sorting rules in the way: [ ['fieldname1','ASC],['fieldname2','DESC'] ]
                * {list} Return results.
        """
        pass
        
    @abstractmethod 
    def get_data_by_conditions_full(self, conditions, sorting_rules, maxRows):
        """
            Makes a Request to the DB manager with a list of conditions, sorting rules and maximum number of results 
                * conditions {list} conditions to all results to be obtained
                * sorting_rules {list} stantard sorting rules in the way: [ ['fieldname1','ASC],['fieldname2','DESC'] ]
                * maxRows {int} maximum number of results to be obtained
                * {list} Return results.
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
    def delete_data_by_conditions(self, conditions):
        """
            Executes a delete statement to the DB manager with a list of conditions.
                * conditions {list} conditions imposed to all rows to be deleted
        """
        pass
          
    @abstractmethod 
    def insert_data(self, var):
        """
            Adds to our database all variables passed as arguments
            * var {list} 
        """
        pass
        