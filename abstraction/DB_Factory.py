from __future__ import print_function
import pysolr
import re
import sys

# Importing specific DB managers
# It's better to use references from root to avoid problems when the script is used from another module
#sys.path.insert(0, '../solr')
sys.path.insert(0, '../../resource-contextualization-import-db/solr')


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
    
        
             
    def get_specific_db_manager(self,DB_TYPE):
        """
            Returns one instance of a database manager pointing to the default dataset/database.
            None if there is any problem creating it.
            * DB_TYPE {string} one of the DB suppliers included in _DB_TYPES.
            * {AbstractManager} Return asked DB manager.
        """
        
        return self.get_specific_db_manager_and_schema(DB_TYPE,None)
    
    
    def get_specific_db_manager_with_user(self,DB_TYPE, username, passw):
        """
            Returns one instance of a database manager pointing to the default dataset/database.
            None if there is any problem creating it.
            * DB_TYPE {string} one of the DB suppliers included in _DB_TYPES.
            * username {string} specific username to use.
            * passw {string} password for the username.
            * {AbstractManager} Return asked DB manager.
        """
        
        return self.get_specific_db_manager_and_schema_and_user(DB_TYPE,None, username, passw)
    
      
        
    def get_specific_db_manager_and_schema(self,DB_TYPE,ds_name):
        """
            Returns one instance of a database manager. None if there is any problem creating it.
            * DB_TYPE {string} one of the DB suppliers included in _DB_TYPES.
            * db_name {string} specific database name to use. None to use default.
            * {AbstractManager} Return asked DB manager.
        """        

        return self.get_specific_db_manager_and_schema_and_user(DB_TYPE, ds_name, None, None)
        
        
    def get_specific_db_manager_and_schema_and_user(self,DB_TYPE,ds_name, username, passw):
        """
            Returns one instance of a database manager. None if there is any problem creating it.
            * DB_TYPE {string} one of the DB suppliers included in _DB_TYPES.
            * db_name {string} specific database name to use. None to use default.
            * username {string} specific username to use.
            * passw {string} password for the username.
            * {AbstractManager} Return asked DB manager.
        """        

        if DB_TYPE == _DB_TYPES[0]:
            return SolrManager(ds_name, username, passw)
        else:
            return None   
    
    
    def get_default_db_manager(self, ds_name):
        """
            Returns one instance of our current database manager pointing to one specific dataset/database.
            None if there is any problem creating it.
            * ds_name {string} specific database name to use. None to use default.
            * {AbstractManager} Return current DB manager.

        """  
        return self.get_specific_db_manager_and_schema(_INSTANCE_TYPE, ds_name)
    
    
    def get_default_db_manager_with_username(self, ds_name, username, passw):
        """
            Returns one instance of our current database manager pointing to one specific dataset/database.
            None if there is any problem creating it.
            * ds_name {string} specific database name to use. None to use default.
            * username {string} specific username to use.
            * passw {string} password for the username.
            * {AbstractManager} Return current DB manager.

        """  
        return self.get_specific_db_manager_and_schema_and_user(_INSTANCE_TYPE, ds_name, username, passw)
       
       
    
    
    
def example():
    """
        Executes one example showing all data from our default DB.        
    """
    my_db_factoy = DBFactory()
    print ("DB Factoy:")
    print (my_db_factoy)
    dbmanager = my_db_factoy.get_default_db_manager('contextData')
    print ("DB Manager:")
    print (dbmanager)
    ourdata = dbmanager.get_all_data()
    print ("Data obtained:")
    print (ourdata)



if __name__ == "__main__":    
    example()
