#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import sys
import os
import mongoengine as me
from mongoengine import NotUniqueError
from mongoengine import DoesNotExist
import bson

import helper

# set environment variable so the right (testing) db is chosen
# compare: <https://github.com/MongoEngine/mongoengine/issues/607>
os.environ['FLASK_ANNOHUB_TESTING'] = '1'

# make imports work, regardless of the path where this is called from
current_dir=os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(os.path.expanduser(os.path.join(current_dir, '../../../app/')))
sys.path.append(path)

from annohub import app

db = me.connect(app.config['MONGODB_SETTINGS']['db'])


# test specific stuff beginns here
from annohub.lib import user
from annohub.models.user import User
#from annohub.lib import language
#from annohub.lib import tagset
#from annohub.lib import genre
from annohub.lib import project


class TestCreateUser(unittest.TestCase):
    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
        self.username = "test"
        self.email = "test@foobar.tld"
        self.password = "test"

    def test_create_user(self):
        user_id = user.create_user(self.username, self.email, self.password)
        self.assertTrue(bson.objectid.ObjectId.is_valid(user_id))
        with self.assertRaises(NotUniqueError):
            user_id = user.create_user(self.username, self.email, self.password)

    def tearDown(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

class TestGetById(unittest.TestCase):
    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
        self.username = "test"
        self.email = "test@foobar.tld"
        self.password = "test"

    def test__get_by_id(self):
        # get a non existing user
        this_user = user._get_by_id(bson.objectid.ObjectId())
        self.assertIsNone(this_user)

        # create the user
        user_id = user.create_user(self.username, self.email, self.password)
        self.assertIsNotNone(user_id)

        # get it
        this_user = user._get_by_id(user_id)
        self.assertIsNotNone(user_id)
        self.assertEqual(user_id, this_user.id)
        self.assertIsInstance(this_user, User)

    def test_get_by_id(self):
        # get a non existing user
        with self.assertRaises(DoesNotExist):
            this_user = user.get_by_id(bson.objectid.ObjectId())

        # create the user
        user_id = user.create_user(self.username, self.email, self.password)
        self.assertIsNotNone(user_id)

        # get it
        this_user = user.get_by_id(user_id)
        self.assertIsNotNone(user_id)
        self.assertEqual(user_id, this_user.id)
        self.assertIsInstance(this_user, User)

    def tearDown(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

class TestGetByName(unittest.TestCase):
    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
        self.username = "test"
        self.email = "test@foobar.tld"
        self.password = "test"

    def test__get_by_name(self):
        # get a non existing user
        this_user = user._get_by_name(self.username)
        self.assertIsNone(this_user)

        # create the user
        this_user = user.create_user(self.username, self.email, self.password)
        self.assertIsNotNone(this_user)

        # get it
        this_user = user._get_by_name(self.username)
        self.assertIsNotNone(this_user)
        self.assertEqual(self.username, this_user.name)
        self.assertIsInstance(this_user, User)

    def test_get_by_name(self):
        # get a non existing user
        with self.assertRaises(DoesNotExist):
            this_user = user.get_by_name(self.username)

        # create the user
        this_user = user.create_user(self.username, self.email, self.password)
        self.assertIsNotNone(this_user)

        # get it
        this_user = user.get_by_name(self.username)
        self.assertIsNotNone(this_user)
        self.assertEqual(self.username, this_user.name)
        self.assertIsInstance(this_user, User)

    def tearDown(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

class TestGetByEmail(unittest.TestCase):
    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
        self.username = "test"
        self.email = "test@foobar.tld"
        self.password = "test"

    def test__get_by_email(self):
        # get a non existing user
        this_user = user._get_by_email(self.email)
        self.assertIsNone(this_user)

        # create the user
        this_user = user.create_user(self.username, self.email, self.password)
        self.assertIsNotNone(this_user)

        # get it
        this_user = user._get_by_email(self.email)
        self.assertIsNotNone(this_user)
        self.assertEqual(self.email, this_user.email)
        self.assertIsInstance(this_user, User)

    def test_get_by_email(self):
        # get a non existing user
        with self.assertRaises(DoesNotExist):
            this_user = user.get_by_email(self.email)

        # create the user
        this_user = user.create_user(self.username, self.email, self.password)
        self.assertIsNotNone(this_user)

        # get it
        this_user = user.get_by_email(self.email)
        self.assertIsNotNone(this_user)
        self.assertEqual(self.email, this_user.email)
        self.assertIsInstance(this_user, User)

    def tearDown(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

class TestSetCreator(unittest.TestCase, helper.HasProject):

    def setUp(self):
        helper.HasProject.setUp(self)

    def test_set_creator(self):
        user._set_creator(self.this_project, self.this_user)
        self.assertEqual(user.get_by_id(self.user_id).creator[0].id, self.project_id)

    def tearDown(self):
        helper.HasProject.tearDown(self)

class TestGetAllByCreator(unittest.TestCase, helper.HasProject):

    def setUp(self):
        helper.HasProject.setUp(self)
        project.set_creator(self.this_project, self.this_user)

    def test_get_all_by_creator(self):
        self.assertEqual(len(user.get_all_by_creator(self.user_id)), 1)
        self.assertEqual(user.get_by_id(self.user_id).creator[0].id, self.project_id)

    def tearDown(self):
        helper.HasProject.tearDown(self)
        #pass

class TestIsCreator(unittest.TestCase, helper.HasProject):

    def setUp(self):
        helper.HasProject.setUp(self)
        project.set_creator(self.this_project, self.this_user)

    def test_is_creator(self):
        self.assertTrue(user.is_creator(self.project_id, self.user_id))

    def tearDown(self):
        #helper.HasProject.tearDown(self)
        pass

class TestSetAnnotator(unittest.TestCase, helper.HasProject):

    def setUp(self):
        helper.HasProject.setUp(self)

    def test_set_annotator(self):
        user._set_annotator(self.this_project, self.this_user)
        self.assertEqual(user.get_by_id(self.user_id).annotator[0].id, self.project_id)

    def tearDown(self):
        helper.HasProject.tearDown(self)

class TestIsAnnotator(unittest.TestCase, helper.HasProject):

    def setUp(self):
        helper.HasProject.setUp(self)
        project.set_annotator(self.this_project, self.this_user)

    def test_is_annotator(self):
        self.assertTrue(user.is_annotator(self.this_project.id, self.this_user.id))

    def tearDown(self):
        helper.HasProject.tearDown(self)
        pass

class TestGetAllByAnnotator(unittest.TestCase, helper.HasProject):

    def setUp(self):
        helper.HasProject.setUp(self)
        user._set_annotator(self.this_project, self.this_user)

    def test_get_all_by_annotator(self):
        self.assertEqual(len(user.get_all_by_annotator(self.user_id)), 1)
        self.assertEqual(user.get_by_id(self.user_id).annotator[0].id, self.project_id)

    def tearDown(self):
        helper.HasProject.tearDown(self)

class TestCheckPassword(unittest.TestCase):
    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
        self.username = "test"
        self.email = "test@foobar.tld"
        self.password = "test"
        user_id = user.create_user(self.username, self.email, self.password)
        self.assertIsNotNone(user_id)

    def test_check_password(self):
        self.assertTrue(user.check_password(self.username, self.password))
        self.assertFalse(user.check_password(self.username, "asdf"))

if __name__ == '__main__':
    unittest.main(verbosity=3, failfast=True)
