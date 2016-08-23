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
import annohub.models.sentence as sentence

class TestAddNotTokenizedSentences(unittest.TestCase):
    def test_add_not_tokenized_sentences(self):
        #def add_not_tokenized_sentences(this_token, text_tokenized):
        self.assertFalse()

class TestRemoveNotTokenizedSentences(unittest.TestCase):
    def test_remove_not_tokenized_sentences(self):
        #def remove_not_tokenized_sentences(this_token):
        self.assertFalse()

class TestAddTokenizedSentences(unittest.TestCase):
    def test_add_tokenized_sentences(self):
        #def add_tokenized_sentences(this_token, text_tokenized):
        self.assertFalse()

class TestAddNotTokenizedSentence(unittest.TestCase):
    def test_add_not_tokenized_sentence(self):
        #def add_not_tokenized_sentence(token_ref, this_sentence, pos):
        self.assertFalse()

# TODO: add the tokenized sentences and incement the pos field
class TestAddTokenizedSentence(unittest.TestCase):
    def test_add_tokenized_sentence(self):
        #def add_tokenized_sentence(token_ref, this_sentence, pos):
        self.assertFalse()

class TestGetNotTokenizedSentences(unittest.TestCase):
    def test_get_not_tokenized_sentences(self):
        #def get_not_tokenized_sentences(this_token, this_limit=app.config['SENTENCE_LIMIT']):
        self.assertFalse()

class TestGetNotAnnotatedSentences(unittest.TestCase):
    def test_get_not_annotated_sentences(self):
        #def get_not_annotated_sentences(annotation, this_limit=app.config['SENTENCE_LIMIT']):
        self.assertFalse()

class TestSkipTokenization(unittest.TestCase):
    def test_skip_tokenization(self):
        #def skip_tokenization(this_project):
        self.assertFalse()

class TestGetNotTokenizedSentence(unittest.TestCase):
    def test_get_not_tokenized_sentence(self):
        #def get_not_tokenized_sentence(this_token):
        self.assertFalse()

class TestDeleteAllByTokenid(unittest.TestCase):
    def test_delete_all_by_tokenid(self):
        #def delete_all_by_tokenid(token_ref):
        self.assertFalse()

