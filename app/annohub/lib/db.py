# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from annohub import app
import annohub.lib.user as user
import annohub.lib.license as license
import annohub.lib.language as language
import annohub.lib.genre as genre
import annohub.lib.tagset as tagset
import annohub.models.project as project_model
import annohub.models.user as user_model
import annohub.models.sentence as sentence_model
from time import localtime, strftime
from mongoengine import connect
import nltk
import string
import re
import os

class Db(object):

    def __init__(self):
        self.now =  strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.db = connect(app.config['MONGODB_SETTINGS']['db'])

    def _default_user(self):
        app.logger.debug("Inserting default user")
        user.create_user(app.config['DEFAULT_USER'], app.config['DEFAULT_USER_EMAIL'], app.config['DEFAULT_USER'])

    def _nltk_setup(self):
        #app.logger.debug(app.config['NLTK_DATA_DIR'])
        app.logger.debug("Updating/downloading nltk data")
        if not os.path.isdir(app.config['NLTK_DATA_DIR']):
            os.mkdir(app.config['NLTK_DATA_DIR'])
        for i in app.config['NLTK_DOWNLOAD']:
            nltk.download(i, download_dir=app.config['NLTK_DATA_DIR'])

    def _license_setup(self):
        app.logger.debug("Inserting licenses")
        for this_license in license.get_all_from_github():
            license.create(this_license['key'], this_license['name'], this_license['url'])

    def _make_name(self, name):
        return string.capwords(re.sub('_', ' ', name))

    def setup(self):
        ''' set up the db for the first time
        - drop everything
        - populate with default data
        - get licenses via github
        - get nltk data
        - set up testing-user
        '''
        self._drop()

        self._license_setup()
        self._nltk_setup()

        app.logger.debug("Inserting languages")
        for key in app.config['LANGUAGES']:
            language.create(key, self._make_name(key))

        app.logger.debug("Inserting genres")
        for key in app.config['GENRES']:
            genre.create(key, self._make_name(key))

        # load tagsets
        tagsets = {}
        for key in app.config['TAGSETS']:
            tagsets[key] = nltk.data.load("help/tagsets/%s.pickle" % key)

        app.logger.debug("Inserting tagsets")
        for key, this_tagset in tagsets.items():
            tagset.create(key, self._make_name(key), this_tagset)

        self._default_user()

    def reset(self):
        ''' removes documents and users for a fresh start
        - removes user and documents
        - imports default user again
        '''

        project_model.Token.drop_collection()
        project_model.Project.drop_collection()
        project_model.Annotation.drop_collection()
        project_model.Stats.drop_collection()

        user_model.User.drop_collection()

        sentence_model.SentenceNotTokenized.drop_collection()
        sentence_model.SentenceTokenized.drop_collection()
        sentence_model.SentenceAnnotated.drop_collection()
        sentence_model.SentenceNotAnnotated.drop_collection()

        self._default_user()

    def _drop(self):
        ''' drops the db '''
        self.db.drop_database(app.config['MONGODB_SETTINGS']['db'])

