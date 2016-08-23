# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from werkzeug.security import generate_password_hash, \
    check_password_hash
import annohub.models.project as project_model
import annohub.models.user as user_model
import bson
#import annohub.lib.project as project
#from annohub import app
#from annohub import app
import annohub.lib.error as e

# these function separate the user operations into its own class connected with
# db-operations and provide an interface that is usable by other components
# all the db-operations use asserts, so the model does not have to

def create_user(name, email, password):
    u''' interface to create a user with name, email and password'''
    assert isinstance(name, basestring)
    assert isinstance(email, basestring)
    assert isinstance(password, basestring)
    assert len(name) > 0
    assert len(email) > 0
    assert len(password) > 0
    password = generate_password_hash(password)
    # never instantiate the user_model.User directly!
    # this function hashes the password aso.
    this_user = user_model.User(name=name, email=email, password=password)
    this_user.save()
    return this_user.id

@e.catchDoesNotExist
def _get_by_name(name):
    return get_by_name(name)

def get_by_name(name):
    assert isinstance(name, basestring)
    assert len(name) > 0
    return user_model.User.objects.get(name=name)

@e.catchDoesNotExist
def _get_by_id(this_id):
    return get_by_id(this_id)

def get_by_id(this_id):
    assert bson.objectid.ObjectId.is_valid(this_id)
    return user_model.User.objects.get(id=this_id)

@e.catchDoesNotExist
def _get_by_email(email):
    print email
    return get_by_email(email)

def get_by_email(email):
    assert isinstance(email, basestring)
    assert len(email) > 0
    return user_model.User.objects.get(email=email)

def check_password(name, password):
    assert isinstance(password, basestring)
    assert len(password) > 0

    found_user = _get_by_name(name)

    if found_user:
        # check_password_hash(pwhash, password)
        #app.logger.debug("Is it equal? %s" % check_password_hash(found_user.password, password))
        #app.logger.debug("Found password: %s" % found_user.password)
        return check_password_hash(found_user.password, password)
    else:
        #app.logger.debug("Did not find a user: %s" % name)
        return False

def is_creator(project_id, user_id):
    assert bson.objectid.ObjectId.is_valid(project_id)
    assert bson.objectid.ObjectId.is_valid(user_id)
    return bson.objectid.ObjectId(project_id) in [ this_project.id for this_project in get_all_by_creator(user_id) ]

def is_annotator(project_id, user_id):
    assert bson.objectid.ObjectId.is_valid(project_id)
    assert bson.objectid.ObjectId.is_valid(user_id)
    return bson.objectid.ObjectId(project_id) in [ this_project.id for this_project in get_all_by_annotator(user_id) ]

def get_all_by_creator(user_id):
    u''' return all projects where this user is a creator'''
    assert bson.objectid.ObjectId.is_valid(user_id)
    return get_by_id(user_id).creator

def get_all_by_annotator(user_id):
    assert bson.objectid.ObjectId.is_valid(user_id)
    return get_by_id(user_id).annotator

def _set_creator(project, this_user):
    assert isinstance(this_user, user_model.User)
    assert isinstance(project, project_model.Project)
    u''' append a project_id to the creator array of a user
         in addition to that, the user_id has to be set as
         the creator in the document.
         this function does not check that, that's why it
         should always be called by lib/project.set_creator'''
    if not is_creator(project.id, this_user.id):
        this_user.update(push__creator=project)
        this_user.save()
        return this_user.id
    else:
        pass
        # TODO: user is creator (at least his own data says so)

def _unset_creator(project, this_user):
    assert isinstance(this_user, user_model.User)
    assert isinstance(project, project_model.Project)
    u''' append a project_id to the creator array of a user
         in addition to that, the user_id has to be set as
         the creator in the document.
         this function does not check that, that's why it
         should always be called by lib/project.set_creator'''
    if is_creator(project.id, this_user.id):
        this_user = get_by_id(this_user.id)
        this_user.update(pull__creator=project)
        this_user.save()
        return this_user.id
    else:
        pass
        # TODO: user is creator (at least his own data says so)

def _set_annotator(project, this_user):
    assert isinstance(this_user, user_model.User)
    assert isinstance(project, project_model.Project)
    u''' append a project_id to the annotator array of a user
         in addition to that, the user_id has to be set as
         the annotator in the document.
         this function does not check that, that's why it
         should always be called by lib/project.set_annotator'''
    if not is_annotator(project.id, this_user.id):
        this_user = get_by_id(this_user.id)
        this_user.update(push__annotator=project)
        this_user.save()
        return this_user.id
    else:
        pass
        # TODO: user is annotator (at least his own data says so)

def _unset_annotator(project, this_user):
    assert isinstance(this_user, user_model.User)
    assert isinstance(project, project_model.Project)
    u''' remove project from users annotations'''
    if is_annotator(project.id, this_user.id):
        this_user = get_by_id(this_user.id)
        this_user.update(pull__annotator=project)
        this_user.save()
        return this_user.id
    else:
        pass
        # TODO: user is annotator (at least his own data says so)

