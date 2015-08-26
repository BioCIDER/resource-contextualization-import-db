from __future__ import print_function
import re
import unittest
import sys

# Importing abstract layer
sys.path.insert(0, '../../resource-contextualization-import-db/abstraction')

from DB_Factory import DBFactory



class TestSolrDB(unittest.TestCase):

    def setUp(self):
        self.dbFactory = DBFactory()
        self.dbManager = self.dbFactory.get_specific_db_manager('SOLR','test_core')


    def test_insertion(self):
        print ('> Insertion test')
        self.previous_count = len(self.dbManager.get_all_data())
        # print ('previous count: %i' % (self.previous_count))
        self.dbManager.insert_data({'title':'test title','field':'test-field'})
        self.new_count = len(self.dbManager.get_all_data())
        # print ('new count: %i' % (self.new_count) )
        self.assertEqual(self.previous_count+1, self.new_count)
        
        
    def test_all_deletion(self):
        print ('> All deletion test')
        self.dbManager.insert_data({'title':'test title','field':'test-field'})
        self.dbManager.delete_all_data()
        self.new_count = len(self.dbManager.get_all_data())
        # print ('data count after deletion: %i' % (self.new_count) )
        self.assertEqual(0, self.new_count)

    

if __name__ == '__main__':
    unittest.main()