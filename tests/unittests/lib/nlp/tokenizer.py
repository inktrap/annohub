#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
import mongoengine as me
# from base import Base

# make imports work, regardless of the path where this is called from
current_dir=os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(os.path.expanduser(os.path.join(current_dir, '../../../../app/')))
sys.path.append(path)

import annohub.lib.nlp.tokenizer as tokenizer
from annohub.lib import error as e
from annohub import app
import nltk
app.config.update(TESTING=True,
                  MONGODB_SETTINGS={'db': 'testing'},
                  DEBUG=True
                  )
db = me.connect(app.config['MONGODB_SETTINGS']['db'])

class TestConfigureTokenizer(unittest.TestCase):
    def setUp(self):
        #db.drop_database(app.config['MONGODB_SETTINGS']['db'])
        assert app.config['OTHER_LANGUAGE'] is not None
        self.genre = app.config['GENRES'][0]
        self.language = app.config['LANGUAGES'][0]
        self.available_languages = app.config['LANGUAGES'][:]
        self.available_languages.remove(app.config['OTHER_LANGUAGE'])
        assert app.config['GENRES'] is not None
        self.available_genres = app.config['GENRES'][:]
        self.available_genres.remove(app.config['OTHER_GENRE'])

    def test_main(self):
        with self.assertRaises(e.NlpSentTokenizerMissing):
            tokenizer.ConfigureTokenizer(app.config['OTHER_LANGUAGE'], self.genre).main()
        for language in self.available_languages:
            sent_tokenize, word_tokenize = tokenizer.ConfigureTokenizer(language, self.genre).main()
            self.assertIsInstance(sent_tokenize, nltk.tokenize.punkt.PunktSentenceTokenizer)
            self.assertIsInstance(word_tokenize, nltk.tokenize.treebank.TreebankWordTokenizer)
        for genre in self.available_genres:
            sent_tokenize, word_tokenize = tokenizer.ConfigureTokenizer(self.language, genre).main()
            self.assertIsInstance(sent_tokenize, nltk.tokenize.punkt.PunktSentenceTokenizer)
            self.assertIsInstance(word_tokenize, nltk.tokenize.treebank.TreebankWordTokenizer)

class TestTokenizerBackend(unittest.TestCase):
    def setUp(self):
        genre = app.config['GENRES'][0]
        sent_tokenize, word_tokenize = tokenizer.ConfigureTokenizer('english', genre).main()
        self.tokenizer_backend = tokenizer.TokenizerBackend(sent_tokenize, word_tokenize)
        self.this_text = "Just some text that should be tokenized. Multiple sentences though."
        # this is not like the real text_to_sents!!!
        self.this_sents = [ sent for sent in self.this_text.split(".")]

    def test_text_to_toks(self):
        result = self.tokenizer_backend.text_to_toks(self.this_text)
        self.assertIsInstance(result, list)
        self.assertEquals(len(result), 2)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[1], list)
        self.assertNotEquals(len(result[0]), 0)
        self.assertNotEquals(len(result[1]), 0)

    def test_text_to_sents(self):
        result = self.tokenizer_backend.text_to_sents(self.this_text)
        self.assertIsInstance(result, list)
        self.assertEquals(len(result), 2)
        self.assertIsInstance(result[0], basestring)
        self.assertIsInstance(result[1], basestring)
        self.assertNotEquals(len(result[0]), 0)
        self.assertNotEquals(len(result[1]), 0)
        # this is not like the real text_to_sents!!!
        # split eats the dot
        self.assertNotEquals(result, self.this_sents)

    def test_sents_to_toks(self):
        result = self.tokenizer_backend.sents_to_toks(self.this_sents)
        self.assertIsInstance(result, list)
        self.assertEquals(len(result), 2)
        self.assertIsInstance(result[0], list)
        self.assertIsInstance(result[1], list)
        self.assertNotEquals(len(result[0]), 0)
        self.assertNotEquals(len(result[1]), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
