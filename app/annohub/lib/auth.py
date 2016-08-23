from annohub import app
#from flask import flash, url_for, redirect
from annohub.lib import error as e
from flask.ext.login import current_user
import bson
import annohub.lib.user as user_lib
from functools import wraps

def check_id(project_id):
    u'''check if an id is well-formed'''
    if not bson.objectid.ObjectId.is_valid(project_id):
        app.logger.debug("Malformed objectid: %s" % str(project_id))
        return False
    return True

def not_allowed(message=None):
    u''' this function will be called if the action is forbidden'''
    # the error is caught by render_exception
    # or by render_js_exception which is handled by js
    if message is None:
        raise e.NotAllowedException()
    else:
        raise e.NotAllowedException(message)

def is_creator(project_id, user_id):
    # check if the user is the creator for this project
    if user_lib.is_creator(project_id, user_id):
        return True
    else:
        return False

def is_annotator(project_id, user_id):
    if user_lib.is_annotator(project_id, user_id):
        return True
    else:
        return False

def is_none():
    app.logger.debug("Denied for everyone")
    return False


# a decorator that checks if the user has the right role
def has_role(role):

    #app.logger.debug("Checking the role of: %s" % role)
    if role not in ['annotator', 'creator', 'any', 'none']:
        raise ValueError

    def choose_decorator(f):
        @wraps(f)
        def check_role(*args, **kwargs):
            is_allowed = False
            if not current_user.is_authenticated:
                app.logger.debug("User not authenticated")
                return not_allowed("Please log in")
            else:
                user_id = current_user.id

            if not 'project_id' in kwargs:
                app.logger.debug("No project id as keyword argument")
                return not_allowed("Internal Error: no project id as keyword argument")
            else:
                project_id = kwargs['project_id']

            ret = check_id(project_id)
            if ret is False:
                app.logger.debug("Invalid project id")
                return not_allowed("Invalid project ID")

            if role == 'any':
                if is_creator(project_id, user_id) or is_annotator(project_id, user_id):
                    is_allowed = True
                formatted_role = "an annotator or creator is"
            if role == 'creator':
                if is_creator(project_id, user_id):
                    is_allowed=True
                formatted_role = "a creator is"
            elif role == 'annotator':
                if is_annotator(project_id, user_id):
                    is_allowed=True
                formatted_role = "annotators are"
            elif role == 'none':
                # TODO: this role is just to test if this works as intended
                # so far, it does :)
                is_allowed = is_none()
                formatted_role = "the member of the empty set is"
            if is_allowed is True:
                return f(*args, **kwargs)
            else:
                app.logger.debug("not allowed")
                return not_allowed("Only %s allowed to do that." % formatted_role)
        return check_role
    return choose_decorator

