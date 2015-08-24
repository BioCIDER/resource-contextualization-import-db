from __future__ import print_function
import pysolr
import re

# Importing specific DB managers
sys.path.insert(0, '../solr')



class DBFactory(object):
    
    _DB_TYPES = ['SOLR']
    
    _INSTANCE_TYPE = _DB_TYPES[0]      # THE CURRENT DB; IT CAN BE ANY OTHER TYPE
    
    
       
    def get_db_manager():
        """
            Returns one instance of our current database manager. None if there is any problem creating it.
            * {AbstractManager} Return current DB manager.
        """        

        if _INSTANCE_TYPE == _DB_TYPES[0]:
            return SolrManager()
        else:
            return None   
    
    
    
def example():
    """
        Executes one example showing all data from our default DB.        
    """
    my_db_factoy = DBFactory()
    dbmanager = my_db_factoy.get_db_manager()
    ourdata = dbmanager.get_all_data()
    print (ourdata)



if __name__ == "__main__":    
    example()
