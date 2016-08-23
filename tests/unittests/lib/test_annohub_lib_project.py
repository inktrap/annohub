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
from annohub.lib import language
from annohub.lib import tagset
from annohub.lib import genre
from annohub.lib import user

app.config.update(TESTING=True,
                  MONGODB_SETTINGS={'db': 'testing'},
                  DEBUG=True
                  )
db = me.connect(app.config['MONGODB_SETTINGS']['db'])

# test specific stuff beginns here
from annohub.lib import project
#from annohub.models.project import Project

class TestCreateProject(unittest.TestCase):
    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

        # insert genre language and a tagset for this project
        self.name = "This is just a name i came up with."
        self.language = language.create('esperanto', 'Esperanto')
        self.genre = genre.create('poems', 'Poems')
        self.tagset_dict = {'N': ('a noun', 'frisbee, table, unicorn')}
        self.tagset_name = 'unicorn'
        self.tagset_title = 'MySpecialUnicornTagset'
        self.tagset = tagset.create(self.tagset_name, self.tagset_title, self.tagset_dict)
        # create token for the project
        self.tokenized_text = [["An", "apple", "a", "day", "."],["Keeps", "the", "doctor", "away", "."]]
        self.num_sentences = len(self.tokenized_text)
        self.token_id = project.create_token(self.tokenized_text, self.num_sentences)
        self.assertIsNotNone(self.token_id)

        # insert a user for this project
        self.username = "test"
        self.email = "test@foobar.tld"
        self.password = "test"
        self.user_id = user.create_user(self.username, self.email, self.password)

    def test_create_project(self):
        #params: creator, name, language, genre, tagset, token_id
        self.project_id = project.create_project(self.user_id,
                self.name,
                self.language,
                self.genre,
                self.tagset,
                self.token_id)
        self.assertTrue(bson.objectid.ObjectId.is_valid(self.project_id))

    def tearDown(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

class TestCreateToken(unittest.TestCase):
    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
        self.tokenized_text = [["An", "apple", "a", "day", "."],["Keeps", "the", "doctor", "away", "."]]
        self.num_sentences = len(self.tokenized_text)

    def test_create_token(self):
        #params: tokenized_text, num_sentences
        token_id = project.create_token(self.tokenized_text, self.num_sentences)
        self.assertTrue(bson.objectid.ObjectId.is_valid(token_id))

    def tearDown(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

#class TestGetAnnotators(unittest.TestCase):
#    def test_get_annotators(self):
#        #project_id):
#        pass
#
#class TestGetCreator(unittest.TestCase):
#    def test_get_creator(self):
#        #project_id):
#        pass
#
#class TestGetProject_by_id(unittest.TestCase):
#    def test_get_project_by_id(self):
#        #project_id):
#        pass
#
#class TestGetToken_by_id(unittest.TestCase):
#    def test_get_token_by_id(self):
#        #token_id):
#        pass
#
#class Test_deleteProject_by_id(unittest.TestCase):
#    def test__delete_project_by_id(self):
#        #project_id):
#        pass
#
#class Test_deleteToken_by_id(unittest.TestCase):
#    def test__delete_token_by_id(self):
#        #token_id):
#        pass
#
#class TestDeleteProject_by_id(unittest.TestCase):
#    def test_delete_project_by_id(self):
#        #project_id):
#        pass
#
#class Test_projectSet_creator(unittest.TestCase):
#    def test__project_set_creator(self):
#        #user_id, project_id):
#        pass
#
#class TestSetCreator(unittest.TestCase):
#    def test_set_creator(self):
#        #user_id, project_id):
#        pass
#
#class TestSetAnnotator(unittest.TestCase):
#    def test_set_annotator(self):
#        #user, project_id):
#        pass

if __name__ == '__main__':
    unittest.main()
