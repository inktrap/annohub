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
from annohub.lib import language

class TestCreate(unittest.TestCase):

    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
        self.this_name = 'name'
        self.this_title = 'title'

    def test_create(self):
        #print(language.create(self.this_name, self.this_title))
        this_language = language.create(self.this_name, self.this_title)
        self.assertTrue(bson.objectid.ObjectId.is_valid(this_language))
        this_language = language.create(self.this_name, self.this_title)
        self.assertIsNone(this_language)

    def tearDown(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])


# class TestGetByKey(unittest.TestCase):
#    def test_get_by_name(self):
# self.assertEqual(expected, get_by_name(language))
# assert False # TODO: implement your test here
#
# class TestGetById(unittest.TestCase):
#    def test_get_by_id(self):
# self.assertEqual(expected, get_by_id(language_id))
# assert False # TODO: implement your test here
#
# class TestGetAll(unittest.TestCase):
#    def test_get_all(self):
# self.assertEqual(expected, get_all())
# assert False # TODO: implement your test here
os.environ['FLASK_ANNOHUB_TESTING'] = '0'

if __name__ == '__main__':
    unittest.main()
