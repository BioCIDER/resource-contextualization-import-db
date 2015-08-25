from __future__ import print_function
import pysolr
import re
import sys

# Importing specific DB managers
sys.path.insert(0, '../solr')
from Solr_Manager import SolrManager

"""
    Class designed to obtain the current DB Manager.
"""
class DBFactory(object):
    
    
    def __init__(self):
        global _DB_TYPES            # DATABASES SUPPORTED BY THIS DBFACTORY
        global _INSTANCE_TYPE       # THE CURRENT DB; IT CAN BE ANY OTHER TYPE
        
        _DB_TYPES = ['SOLR']
        _INSTANCE_TYPE = _DB_TYPES[0]
        
        
    def __str__(self):
        return "DBFactory, current DB: %s" % (_INSTANCE_TYPE)
    
        
    def get_db_manager(self,DB_TYPE):
        """
            Returns one instance of a database manager. None if there is any problem creating it.
            * {AbstractManager} Return asked DB manager.
        """        

        if DB_TYPE == _DB_TYPES[0]:
            return SolrManager()
        else:
            return None   
    
    
    def get_my_db_manager(self):
        """
            Returns one instance of our current database manager. None if there is any problem creating it.
            * {AbstractManager} Return current DB manager.
        """  
        
        return self.get_db_manager(_INSTANCE_TYPE)
       
       
    
    
    
def example():
    """
        Executes one example showing all data from our default DB.        
    """
    my_db_factoy = DBFactory()
    print ("DB Factoy:")
    print (my_db_factoy)
    dbmanager = my_db_factoy.get_my_db_manager()
    print ("DB Manager:")
    print (dbmanager)
    ourdata = dbmanager.get_all_data()
    print ("Data obtained:")
    print (ourdata)



if __name__ == "__main__":    
    example()
