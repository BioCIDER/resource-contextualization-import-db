from __future__ import print_function
import pysolr
import re
import sys

# Importing abstract layer
#sys.path.insert(0, '../abstraction')
sys.path.insert(0, '../../resource-contextualization-import-db/abstraction')

from Abstract_Manager import AbstractManager


"""
    Specific class to support Solr DB. Implements functionality of AbstractManager class.
"""
class SolrManager(AbstractManager):
    
    
    def _create_instance(self):
        """
            It tries to create a new instance of solr database.
            * Returns current solr instance. None if there was any problem creating it.           
        """
        
        # global _solrLocal       # instance of our solr database

        try:
            self._solrLocal = pysolr.Solr(self.getUrl(), self.getTimeout())
        except Exception as e:
            print ("Exception trying to access Solr instance:")
            print (e)
            self._solrLocal =  None 
    
    
    def __init__(self, ds_name):
        """
            Initialization function.
            * db_name {string} specific core name to use. None to use default.
        """
        
        if ds_name is None:
            self.url = 'http://localhost:8983/solr/eventsData'
        else:
            self.url = 'http://localhost:8983/solr/'+ds_name
        self.timeout = 10
        self._create_instance()
    
    
    #def __init__(self, url, timeout):
    #    self.url = name
    #    self.timeout = timeout
    
    def getUrl(self):
        return self.url

    def getTimeout(self):
        return self.timeout

    def __str__(self):
        return "%s with timeout of %i" % (self.url, self.timeout)
    
    
    
    def _get_instance(self):
        """
            Returns the singleton instance of solr database.
            NOT RECOMMENDED: only this class functionality should be used. It allows specific solr DB operations.
            * Returns current specific solr controller. None if there is any problem creating it.           
        """
        
        if (self._solrLocal is None):
            self._create_instance()
            
        return self._solrLocal
    
    
    
    # BASIC OPERATIONS
    
    def get_all_data(self):
        """
            Makes a Request to the Solr Server from "localhost"
                * {list} Return results.
        """
        my_instance = self._get_instance()
        if my_instance is not None:
            try:                
                resultsLocal = my_instance.search(q='*:*', rows='5000')
                return resultsLocal
            except Exception as e:
                print ("Exception trying to get Solr data")
                print (e)
                return None
        else:
            return None
        
    
    def _get_data_by(self, condition):
        """
            Makes a Request to the local Solr Server with some condition.
            NOT RECOMMENDED.
                * condition {string} condition of all results to be obtained
                * {list} Return results.
        """
        my_instance = self._get_instance()
        if my_instance is not None:
            try:                
                resultsLocal = my_instance.search(q=condition, rows='5000')
                return resultsLocal
            except Exception as e:
                print ("Exception trying to get Solr data")
                print (e)
                return None
        else:
            return None
    
    
    def delete_all_data(self):
        """
            Delete all the data from DB
        """
        my_instance = self._get_instance()
        if my_instance is not None:
            try:
                my_instance.delete(q='*:*')
            except Exception as e:
                print ("Exception trying to delete Solr data")
                print (e)
    
    
    def insert_data(self, mydata):
        """
            Adds to our database all variables passed as arguments
            * mydata {list} 
        """
        my_instance = self._get_instance()
        if my_instance is not None:
            try:
                my_instance.add([
                    mydata
                ])
            except Exception as e:
                print ("Exception trying to inser Solr data")
                print (e)
    
    
    
    
    
    
def example():
    """
        Executes one example showing all data from our solr DB.
        
    """
    from SolrManager import SolrManager
    solrmanager = SolrManager()
    # ourdata = solrmanager.get_all_data()
    ourdata = solrmanager.get_data_by('disease')
    print (ourdata)


if __name__ == "__main__":
    example()
