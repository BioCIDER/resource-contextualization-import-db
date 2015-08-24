from __future__ import print_function
import pysolr
import re

# Importing abstract layer
sys.path.insert(0, '../abstraction')
import AbstractManager


"""
    Specific class to support Solr DB. Implements functionality of AbstractManager class.
"""
class SolrManager(AbstractManager):
    
    # Private instance of our solr database
    _solrLocal
    
    def __init__(self):
        self.url = 'http://localhost:8983/solr/eventsData'
        self.timeout = 10
        _create_instance()
    
    #def __init__(self, url, timeout):
    #    self.url = name
    #    self.timeout = timeout
    
    def getUrl(self):
        return self.url

    def getTimeout(self):
        return self.timeout

    def __str__(self):
        return "%s is a %i" % (self.url, self.timeout)
    
    
    def _create_instance():
        """
            It tries to create a new instance of solr database.
            * Returns current solr instance. None if there was any problem creating it.           
        """
        
        try:
            _solrLocal = pysolr.Solr(getUrl(), getTimeout())
        except Exception:
            print ("Exception trying to access Solr instance")
            _solrLocal =  None 
    
    
    def get_instance():
        """
            Returns the singleton instance of solr database.
            NOT RECOMMENDED: only this class functionality should be used. It allows specific solr DB operations.
            * Returns current specific solr controller. None if there is any problem creating it.           
        """
        
        if (_solrLocal is None):
            _create_instance()
            
        return _solrLocal
    
    
    
    # BASIC OPERATIONS
    
    def get_all_data():
        """
            Makes a Request to the Solr Server from "localhost"
                * solrLocal {class} url - Uniform Resource Locator
                * resultsLocal {class} Query operator:
                    "q='*:*'" - Query all the data;
                    "rows='5000'" - Indicates the maximum number of events that will be returned;
        """
        resultsLocal = solrLocal.search(q='*:*', rows='5000')
    
    
    def delete_all_data():
        """
            Delete all the data from DB
        """
        
        solrLocal.solrLocal.delete(q='*:*')
    
    
    def insert_data(var):
        """
            Adds to our database all variables passed as arguments"
            * var {list} 
        """
        
        solrLocal.add([
            vars
        ])
    
    
    
    
    
def example():
    """
        Executes one example showing all data from our solr DB.
        
    """
    solrmanager = SolrManager()
    ourdata = solrmanager.get_all_data()
    print (ourdata)


if __name__ == "__main__":
    example()
