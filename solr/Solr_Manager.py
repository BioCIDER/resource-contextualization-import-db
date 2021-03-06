from __future__ import print_function

import pysolr
# import requests # it's the internal class for connections used by pysolr.
import urllib2
import re
import sys
import logging

from pprint import pprint

# Importing abstract layer
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
        
        try:
	    self._solrLocal = pysolr.Solr(self.getUrl(), timeout=self.getTimeout())
            mysession = self._solrLocal.session	   # We obtain the local session in order to change its behavour
            #mysession.auth = auth  # Authentication can be done also like this: auth = ('user', 'pass')
            # For some reason, the certificate cannot be validated from our own server! validation has to be disabled in this case  
            mysession.verify = False
        except Exception as e:
            self.logger.critical("Exception trying to access Solr instance:")
            self.logger.critical(e)
            self._solrLocal =  None 
    
    
    def __init__(self, ds_name, username, passw):
        """
            Initialization function.
            * db_name {string} specific core name to use. None to use default.
        """
        super(SolrManager, self).__init__()
        

	authString = ''

        if username is not None and passw is not None :
            authString = username+':'+passw+'@'

        if ds_name is None:
#       	   self.url = 'https://biocider.org:8983/solr/contextData'     
	   self.url = 'https://'+authString+'biocider.org:8983/solr/contextData' 
	   # self.url = 'https://'+authString+'localhost:8983/solr/contextData'
        else:
	   #self.url = 'https://biocider.org:8983/solr/'+ds_name              
           self.url = 'https://'+authString+'biocider.org:8983/solr/'+ds_name
	   # self.url = 'https://'+authString+'localhost:8983/solr/'+ds_name
        

	self.timeout = 10
        self._create_instance()
    
    
    def getUrl(self):
        return self.url

    def getTimeout(self):
        return self.timeout

    def __str__(self):
        return "%s with timeout of %i" % (self.url, self.timeout)
    
    
    
    def _get_instance(self):
        """
            Returns the singleton instance of solr database.
            NOT RECOMMENDED: It allows specific solr DB operations, to use in very specific situations.
            You should use normal CRUD functionality available in this class instead. 
            * Returns current specific solr controller. None if there is any problem creating it.           
        """
        
        if (self._solrLocal is None):
            self._create_instance()
            
        return self._solrLocal
    
    
       
    def _get_solr_condition(self, condition):
        """
            Transforms one standard condition to one SolR condition.
                * condition {list} one stantard condition
                * {string} Solr condition.
        """
        solr_condition = ''
        if condition is not None:
            try:
                self.logger.debug ('Condition: ')
                self.logger.debug (condition)
                
                # WE HAVE TO SEE IF EQ, NO OR OTHERS CAN HAVE MORE CONDITIONS INSIDE THEM
                if condition[0] == self.OPERATORS[0]:     # EQ
                                        # It never has more conditions inside, but it can receive a list of values!
                    if ( isinstance(condition[2], basestring)):
                        solr_condition = condition[1]+':"'+condition[2]+'"'
                    else:   # We have a list of terms
                        listOfTerms = condition[2]
                        partial_solr_condition = ""
                        for conditionTerm in listOfTerms:
                            if len(partial_solr_condition)>1:
                                #commented lines are a different kind of condition, not exclusive
                                #partial_solr_condition = partial_solr_condition+" AND "+condition[1]+':"'+conditionTerm+'" '
                                partial_solr_condition = partial_solr_condition+' AND "'+conditionTerm+'" '

                            else:
                                #partial_solr_condition = condition[1]+':"'+conditionTerm+'" '
                                partial_solr_condition = condition[1]+':("'+conditionTerm+'" '

                        #solr_condition = '('+partial_solr_condition+')'
                        solr_condition = partial_solr_condition+')'   
                        
                elif condition[0] == self.OPERATORS[1]:   # NO      It CAN have more conditions inside
                    if ( not isinstance(condition[1], basestring)):  # If condition[1] is other condition list...
                        solr_condition = 'NOT ('+self._get_solr_conditions_by_parent_condition(condition[1],condition)+')'    
                    else:
                        solr_condition = 'NOT ('+condition[1]+': "'+condition[2]+'")'
                    
                    
                elif condition[0] == self.OPERATORS[2]:   # AND     It will have always more conditions inside
                    solr_condition = '('+self._get_solr_conditions(condition[1])+')'
                elif condition[0] == self.OPERATORS[3]:   # OR.     It will have always more conditions inside
                    solr_condition = '('+self._get_solr_conditions_by_parent_condition(condition[1],condition)+')'    
                    
                self.logger.debug ('solr_condition: ')
                self.logger.debug (solr_condition)
                return solr_condition
            except Exception as e:
                self.logger.error("Exception trying to convert one standard condition to SolR condition :"+format(sys.exc_info()[-1].tb_lineno))
                self.logger.error(e)
                return None
        else:
            return '*:*'
        
    
    def _get_solr_conditions(self, conditions):
        return self._get_solr_conditions_by_parent_condition(conditions, None)
        
    def _get_solr_conditions_by_parent_condition(self, conditions, parent_condition):
        """
            Transforms standard conditions to SolR conditions.
                * conditions {list} conditions to all results to be obtained
                * parent_condition {list}  parent condition can influences how its children are concatenated
                * {string} Solr conditions.
        """
        solr_total_condition = ''
        if conditions is not None:
            try:
                
                for condition in conditions:
                    self.logger.debug ('condition in loop:')
                    self.logger.debug(condition)
                    new_solr_condition = self._get_solr_condition(condition)
                    operator = ''
                    if len(solr_total_condition)>1:     # If solr_total_condition already has some condition...
                        if parent_condition is not None:
                            if parent_condition[0] == self.OPERATORS[3]:   # OR
                                operator = ' OR '
                            if parent_condition[0] == self.OPERATORS[1]:   # NO
                                operator = ' AND '
                                
                        if len(operator)==0:            # If we don't depend on parent conditions, our operator can depends on our own condition
                            # Depending on what is the next operator, we can need to join it with other auxiliar operator...
                            if condition[0] == self.OPERATORS[0]:    # EQ
                                operator = ' AND '
                        
                        
                    solr_total_condition = solr_total_condition+' '+operator+' '+new_solr_condition
                    solr_total_condition = solr_total_condition.strip()
                    
                self.logger.debug('Final solr conditions:')
                self.logger.debug(solr_total_condition)
                return solr_total_condition
            except Exception as e:
                self.logger.error("Exception trying to convert standard conditions to SolR conditions")
                self.logger.error(e)
                return None
        else:
            return '*:*'
    
    
    def _get_solr_sorting_rules(self, sorting_rules):
        """
            Transforms standard sorting rules to SolR sorting rules.
                * sorting_rules {list} stantard sorting rules in the way: [ ['fieldname1','ASC],['fieldname2','DESC'] ]
                * {string} Solr sorting rules.
        """
        solr_rules = None
        if sorting_rules is not None and len(sorting_rules)>0:
            try:
                solr_rules = ''
                for sorting_rule in sorting_rules:
                    new_sorting_rule = sorting_rule[0]+' '+sorting_rule[1].lower()
                    
                    if len(solr_rules)>1:
                        solr_rules = solr_rules+' , '
                    
                    solr_rules = solr_rules + new_sorting_rule
                 
                return solr_rules
            except Exception as e:
                self.logger.error("Exception trying to convert standard conditions to SolR conditions")
                self.logger.error(e)
                return None
        else:
            return None  
        
        
        
    
    # BASIC OPERATIONS
    
    def get_all_data(self):
        """
            Makes a Request to the Solr Server from "localhost"
                * {list} Return results.
        """
        my_instance = self._get_instance()
        if my_instance is not None:
            try:
                resultsLocal = my_instance.search(q='*:*')
                return resultsLocal.docs
            except Exception as e:
                self.logger.error("Exception trying to get Solr data")
                self.logger.error(e)
                return None
        else:
            return None
        
    
    
    def get_data_by_conditions(self, conditions):
        """
            Makes a Request to the local Solr Server with a list of conditions.
                * conditions {list} conditions to all results to be obtained
                * {list} Return unsorted results, with a maximum of 5000.
        """
        return self.get_data_by_conditions_full(conditions, None, 5000)
    
    def get_data_by_conditions_sorting(self, conditions, sorting_rules):
        """
            Makes a Request to the local Solr Server with a list of conditions.
                * conditions {list} conditions to all results to be obtained
                * sorting_rules {list} field and direction of sorting results
                * {list} Return results, with a maximum of 5000.
        """
        return self.get_data_by_conditions_full(conditions, sorting_rules ,5000)
       
    def get_data_by_conditions_full(self, conditions, sorting_rules, maxRows):
        """
            Makes a Request to the local Solr Server with a list of conditions.
                * conditions {list} conditions to all results to be obtained
                * sorting_rules {list} field and direction of sorting results
                * maxRows {int} maximum number of results to be obtained
                * {list} Return results.
        """
        my_instance = self._get_instance()
        if my_instance is not None:
            try:
                self.logger.debug('> get data by conditions full:')
                self.logger.debug(conditions)
                
                solr_conditions = self._get_solr_conditions(conditions)               
                self.logger.debug('solr conditions to apply:')
                self.logger.debug(solr_conditions)
                
                solr_rules = self._get_solr_sorting_rules(sorting_rules)
                if solr_rules is None:                   
                    solr_rules = ''
                                       
                if maxRows is not None:
                    resultsLocal = my_instance.search(q=solr_conditions, sort=solr_rules, rows=str(maxRows) )
                else:
                    resultsLocal = my_instance.search(q=solr_conditions, sort=solr_rules)
                return resultsLocal.docs
            except Exception as e:
                self.logger.error("Exception trying to get Solr data")
                self.logger.error(e)
                return None
        else:
            return None
            
    
    def _get_data_by(self, condition):
        """
            Makes a Request to the local Solr Server with some free condition.
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
                self.logger.error("Exception trying to get Solr data")
                self.logger.error(e)
                return None
        else:
            return None
    
    
    
    def count_data_by_conditions(self, conditions):
        """
            Makes a count request to the local Solr Server with a list of conditions.
            It's much faster than count a set of results.
                * conditions {list} conditions to all results to be counted
                * {int} results number.
        """
        my_instance = self._get_instance()
        if my_instance is not None:
            try:
                self.logger.debug('> count data by conditions:')
                self.logger.debug(conditions)
                
                solr_conditions = self._get_solr_conditions(conditions)               
                self.logger.debug('solr conditions to apply:')
                self.logger.debug(solr_conditions)
                
                resultsLocal = my_instance.search(q=solr_conditions)
                # Very useful funtion to dump any object
                # pprint(vars(resultsLocal))
                
                return resultsLocal.hits
            except Exception as e:
                self.logger.error("Exception trying to count Solr data")
                self.logger.error(e)
                return None
        else:
            return None
        
    
    
    def delete_all_data(self):
        """
            Delete all data from DB
        """
        my_instance = self._get_instance()
        
        if my_instance is not None:
            try:
                my_instance.delete(q='*:*')
            except Exception as e:
                self.logger.error("Exception trying to delete Solr data")
                self.logger.error(e)
             
                
                
    def delete_data_by_conditions(self, conditions):
        """
            Executes a delete statement to the SolR DB with a list of conditions.
                * conditions {list} conditions imposed to all rows to be deleted
        """
        my_instance = self._get_instance()
        
        if my_instance is not None:
            try:
                                
                self.logger.debug('> get data by conditions full:')
                self.logger.debug(conditions)
                
                solr_conditions = self._get_solr_conditions(conditions)               
                self.logger.debug('solr conditions to apply:')
                self.logger.debug(solr_conditions)
        
                my_instance.delete(q=solr_conditions)

            except Exception as e:
                self.logger.error("Exception trying to delete Solr data")
                self.logger.error(e)
        
    
    
    def insert_data(self, mydata):
        """
            Adds to our database all variables passed as arguments
            * mydata {list}
            * {boolean} Return operation result.
            
        """
        my_instance = self._get_instance()
        if my_instance is not None:
            try:
                result = my_instance.add([
                    mydata
                ])
                if ('<int name="status">0</int>' in result):
                    return True
                else:
                    return False
            except Exception as e:
                self.logger.error("Exception trying to access Solr instance:")
                self.logger.error(e)
                return False
        return False
    
    
    
    
    
    
def example():
    """
        Executes one example showing all data from our solr DB.
        
    """
    from Solr_Manager import SolrManager
    solrmanager = SolrManager('test_core')
    # ourdata = solrmanager.get_all_data()
    ourdata = solrmanager.get_data_by('disease')
    print (ourdata)


if __name__ == "__main__":
    example()
