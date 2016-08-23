# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from annohub import db
#import mongoengine

class User(db.Document):
    name = db.StringField(max_length=50, required=True, unique=True)
    email = db.StringField(max_length=50, required=True, unique=True)
    password = db.StringField(max_length=75, required=True)
    # the following fields are in '' because:
    # - User will import Token and this avoids circular imports
    # - Token will be created after a user exists
    # - adding and removing documents is handled via annohub.lib.document/user and
    #   will take care of adding/removing/updating the correct type of reference
    annotator = db.ListField(db.ReferenceField('db.Project'), default=list)
    creator = db.ListField(db.ReferenceField('db.Project'), default=list)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name

    def __unicode__(self):
        return u'<User %r>' % self.name

    def __repr__(self):
        return u'<User %r>' % self.name

