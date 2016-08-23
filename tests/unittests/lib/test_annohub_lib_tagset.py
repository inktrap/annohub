#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import sys
import os
import mongoengine as me
import bson

# set environment variable so the right (testing) db is chosen
# compare: <https://github.com/MongoEngine/mongoengine/issues/607>
os.environ['FLASK_ANNOHUB_TESTING'] = '1'

# make imports work, regardless of the path where this is called from
current_dir=os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(os.path.expanduser(os.path.join(current_dir, '../../../app/')))
sys.path.append(path)

from annohub import app

app.config.update(TESTING=True,
                  MONGODB_SETTINGS={'db': 'testing'},
                  DEBUG=True
                  )
db = me.connect(app.config['MONGODB_SETTINGS']['db'])

# test specific stuff beginns here
from annohub.lib import tagset

class TestCreate(unittest.TestCase):

    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
        self.this_dict = {'N': ('a noun', 'frisbee')}
        self.this_name = 'name'
        self.this_title = 'title'

    def test_create(self):
        #print(tagset.create(self.this_name, self.this_title, self.this_dict))
        self.assertTrue(bson.objectid.ObjectId.is_valid(tagset.create(self.this_name, self.this_title, self.this_dict)))
        self.assertIsNone(tagset.create(self.this_name, self.this_title, self.this_dict))

    def tearDown(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

# class TestGetByKey(unittest.TestCase):
#    def setUp(self):
#        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
#        self.tagset_dict = [{'N': ('a noun', 'frisbee')}]
#        self.tagset_name = 'name'
#        self.tagset_title = 'title'
#    def test_get_by_name(self):
#        tagset.create(self.tagset_name, self.tagset_title, self.tagset_dict)
#        expected = [self.tagset_name]
#        self.assertEqual(expected, tagset.get_by_name(self.tagset_name).name)
#    def tearDown(self):
#        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
#
# class TestGetById(unittest.TestCase):
#    def setUp(self):
#        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
#        self.tagset_dict = [{'N': ('a noun', 'frisbee')}]
#        self.tagset_name = 'name'
#        self.tagset_title = 'title'
#    def test_get_by_id(self):
#        this_tagset = tagset.create(self.tagset_name, self.tagset_title, self.tagset_dict)
#        expected = [self.tagset_name]
#        print(tagset.get_by_id(this_tagset).name)
# self.assertEqual(expected, tagset.get_by_id(this_tagset).name)
#    def tearDown(self):
#        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
#
# class TestGetAll(unittest.TestCase):
#    def setUp(self):
#        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
#        self.tagset_dict = [{'N': ('a noun', 'frisbee')}]
#        self.tagset_name = 'name'
#        self.tagset_title = 'title'
#    def test_get_all(self):
#        result = tagset.get_all()
#        print(result)
#        self.assertTrue(isinstance(result, list))
#        self.assertTrue(len(result) > 0)
#    def tearDown(self):
#        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

if __name__ == '__main__':
    unittest.main()
