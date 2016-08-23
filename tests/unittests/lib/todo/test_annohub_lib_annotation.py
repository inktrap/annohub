#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import sys
import os
import mongoengine as me
from mongoengine import NotUniqueError
import bson

# set environment variable so the right (testing) db is chosen
# compare: <https://github.com/MongoEngine/mongoengine/issues/607>
os.environ['FLASK_ANNOHUB_TESTING'] = '1'

# make imports work, regardless of the path where this is called from
current_dir=os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(os.path.expanduser(os.path.join(current_dir, '../../../app/')))
sys.path.append(path)

from annohub import app
#from annohub.lib import language
#from annohub.lib import tagset
#from annohub.lib import genre
#from annohub.lib import user

app.config.update(TESTING=True,
                  MONGODB_SETTINGS={'db': 'testing'},
                  DEBUG=True
                  )
db = me.connect(app.config['MONGODB_SETTINGS']['db'])

# test specific stuff beginns here
from annohub.lib import annotation
#from annohub.models.project import Project

class TestCreateAnnotation(unittest.TestCase):
    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

    def test_create_annotation(self):
        assert False

    def tearDown(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

if __name__ == '__main__':
    unittest.main()
