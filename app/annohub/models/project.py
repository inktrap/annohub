# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from annohub import db
import annohub.models.user as user
import annohub.models.tagset as tagset
import annohub.models.genre as genre
import annohub.models.language as language

# the classes below are connected to Project and represent
# various stages of the project

# this is the new/partly tokenized text (0 and 1)
class Token(db.Document):
    u''' a project with information for tokenization per project'''
    additional = db.IntField(default=0)
    # these are the already tokenized sentences
    tokenized = db.IntField(default=0)
    # these are the sentences that are not tokenized yet
    not_tokenized = db.IntField(min_value=0)
    # the initial amount of not tokenized sentences
    initial_sentences = db.IntField(min_value=1)
    percent = db.FloatField(default=0.0, min_value=0.0)
    # wether a project creator skipped tokenization
    # 0 no 1 yes
    skipped = db.IntField(default=0, choices=(0, 1))

# main project class
# methods for project, token, tags and stats are in lib/project.py

class Project(db.Document):
    u''' this class is the base of every project
    it's id is referenced by token and tags that hold user specific data
    '''
    annotator = db.ListField(db.ReferenceField(user.User), default=list)
    creator = db.ReferenceField(user.User, required=True)
    language = db.ReferenceField(language.Language, required=True)
    genre = db.ReferenceField(genre.Genre, required=True)
    name = db.StringField(required=True)
    tagset = db.ReferenceField(tagset.Tagsets, required=True)
    token = db.ReferenceField(Token, required=True)
    '''
    0 tokenize
    1 manage
    2 annotate
    3 publish
    4 stats
    '''
    status = db.IntField(default=0, choices=(0,1,2,3,4), required=True)

# this is the progress for each annotator
# the default-tags are stored in SentenceNotAnnotated
# the user-tags are stored in SentenceAnnotated
class Annotation(db.Document):
    u''' an annotation that represents the current status per project and annotator'''
    user = db.ReferenceField(user.User, required=True)
    project = db.ReferenceField(Project, required=True)
    token = db.ReferenceField(Token, required=True)
    '''
    0 annotate
    1 stats
    '''
    status = db.IntField(default=0, choices=(0,1), required=True)
    annotated = db.IntField(default=0)
    not_annotated = db.IntField(required=True)
    # the number of sentences is equal to Token.tokenized of the Project
    # did the user skip his annotation? 0 = No 1 = Yes
    # 0 no 1 yes
    skipped = db.IntField(default=0, choices=(0, 1))

## this contains the information about the tags for each annotator, (like Token for each creator)
#class Tags(db.Document):
#    u''' a project with the tags for each project for each annotator'''
#    user = db.ReferenceField(user.User, required=True)
#    tagged = db.IntField(default=0)
#    untagged = db.IntField(required=True)
#    project = db.ReferenceField(Project, required=True)

# info if/how this project is published
class Stats(db.Document):
    u''' contains stats and license and publishing information for a project'''
    # currently not needed:
    is_public = db.BooleanField(default=False, required=True)
    license = db.StringField(max_length=50)

