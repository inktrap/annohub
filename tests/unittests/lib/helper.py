#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import mongoengine as me

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
from annohub.lib import language
from annohub.lib import tagset
from annohub.lib import genre
from annohub.lib import project
import bson

class HasProject(object):
    def setUp(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])

        self.name = "This is just a name i came up with."
        # insert genre language and a tagset for this project
        self.language = language.create('esperanto', 'Esperanto')
        self.genre = genre.create('poems', 'Poems')
        self.tagset_dict = {'N': ('a noun', 'frisbee, table, unicorn')}
        self.tagset_name = 'unicorn'
        self.tagset_title = 'MySpecialUnicornTagset'
        self.tagset = tagset.create(self.tagset_name, self.tagset_title, self.tagset_dict)

        # create token for the project
        #self.text = "An apple a day. Keeps the doctor away."
        self.text_tokenized = [["An", "apple", "a", "day", "."],["Keeps", "the", "doctor", "away", "."]]
        self.num_sentences = len(self.text_tokenized)

        # insert a user for this project
        self.username = "test"
        self.email = "test@foobar.tld"
        self.password = "test"
        self.user_id = user.create_user(self.username, self.email, self.password)
        # create token and text for this project
        #params: tokenized_text, num_sentences
        self.token_id = project.create_token(self.text_tokenized, self.num_sentences)
        self.assertTrue(bson.objectid.ObjectId.is_valid(self.token_id))
        self.project_id = project.create_project(self.user_id,
                self.name,
                self.language,
                self.genre,
                self.tagset,
                self.token_id)
        assert isinstance(self.project_id, bson.objectid.ObjectId)
        self.this_project = project.get_project_by_id(self.project_id)
        self.this_user = user.get_by_id(self.user_id)

    def tearDown(self):
        db.drop_database(app.config['MONGODB_SETTINGS']['db'])
        #pass

if __name__ == '__main__':
    sys.exit(1)
