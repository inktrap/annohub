# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

#import sys
#import re
from annohub import app
from flask import flash
import sys
from functools import wraps
from flask import redirect, render_template, url_for
from mongoengine import DoesNotExist

u'''
convention for error-classes:
    ModulenameLongDescriptionOfProblem(ExceptionParent):
'''

class ExceptionParent(Exception):
    def __init__(self, message="An unknown exception occurred."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class FileutilsInvalidFileEncodingException(ExceptionParent):
    u'see classname'
    def __init__(self, message="The encoding of the file could not be read"):
        self.message = message
    def __str__(self):
        return repr(self.message)

class FileutilsEmptyFileException(ExceptionParent):
    u'see classname'
    def __init__(self, message="The file you provided is empty"):
        self.message = message
    def __str__(self):
        return repr(self.message)

class FileutilsFileTooLargeException(ExceptionParent):
    u'see classname'
    def __init__(self, message="The file you provided is too large and must be smaller than %.1f KB"):
        self.message = message % int(app.config['SIZE_LIMIT'] / 1024.0)
    def __str__(self):
        return repr(self.message)

class FileutilsInvalidFileReadException(ExceptionParent):
    u'see classname'
    def __init__(self, message="The file you provided could not be read."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class NlpSentTokenizerMissing(ExceptionParent):
    u'see classname'
    def __init__(self, message="The tokenizer for this language is not present. File a ticket so this will be fixed."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class NlpTaggerMissing(ExceptionParent):
    u'see classname'
    def __init__(self, message="The tagger for this language is not present. The administrator of this site should download it via nltk.download()."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class CreateProjectUnknownLanguage(ExceptionParent):
    u'see classname'
    def __init__(self, message="The language could not be found in the database. This is an internal error."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class CreateProjectUnknownGenre(ExceptionParent):
    u'see classname'
    def __init__(self, message="The genre could not be found in the database. This is an internal error."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class InvalidDataStructure(ExceptionParent):
    u'see classname'
    def __init__(self, message="The data structure we recieved is invalid."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class InvalidDataValues(ExceptionParent):
    u'see classname'
    def __init__(self, message="The data we recieved is invalid."):
        self.message = message
    def __str__(self):
        return repr(self.message)


class NoMoreSentencesPresent(ExceptionParent):
    u'see classname'
    def __init__(self, message="There are no more sentences present."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class DocumentTooLarge(ExceptionParent):
    u'see classname'
    def __init__(self, message="We processed your document and the result is too large."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class NotAllowedException(ExceptionParent):
    u'see classname'
    def __init__(self, message="The action is forbidden."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class CantTokenize(ExceptionParent):
    u'see classname'
    def __init__(self, message="You can not tokenize this project. Has it been tokenized already?"):
        self.message = message
    def __str__(self):
        return repr(self.message)

class CantPublish(ExceptionParent):
    u'see classname'
    def __init__(self, message="You can not publish this project. You have no annotators or they did not finish their work."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class CantAnnotate(ExceptionParent):
    u'see classname'
    def __init__(self, message="You can not annotate this project."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class NotImplementedFeature(ExceptionParent):
    u'see classname'
    def __init__(self, message="Ooops, this feature is not implemented. Sorry."):
        self.message = message
    def __str__(self):
        return repr(self.message)

class InvalidRoleError(ExceptionParent):
    u'see classname'
    def __init__(self, message="This role is not valid. How could that happen?"):
        self.message = message
    def __str__(self):
        return repr(self.message)

class CantCompleteAction(ExceptionParent):
    u'see classname (the message should be adapted when raising)'
    def __init__(self, message="The action could not be completed."):
        self.message = message
    def __str__(self):
        return repr(self.message)


# the custom exception handler
# this does not work as a replacement for sys.excepthook, because flask handles exceptions
# on its own. instead it is used by the render_exception decorator.
def exceptionHandler(exc_type=None, exc_instance=None, exc_traceback=None):
    if exc_type is None and \
    exc_instance is None and \
    exc_traceback is None:
        exc_type, exc_instance, exc_traceback = sys.exc_info()
    if (app.config['TESTING'] is True):
        return sys.__excepthook__(exc_type, exc_instance, exc_traceback)
    else:
        if isinstance(exc_instance, ExceptionParent):
            try:
                return(exc_type, exc_instance, exc_traceback)
            except RuntimeError:
                print exc_instance.message
            ## TODO: log/mail exception here
        else:
            if app.config['DEBUG']:
                # raise the exception if debugging is on
                raise exc_type, exc_instance, exc_traceback
            # TODO: switch: only return default exception for everything not caught before
            return exceptionHandler(ExceptionParent, ExceptionParent(), exc_traceback)

# an exception decorator that can be freely importet.
# it will call the function, render the specified template if an exception
# occurs and also will populate the form again via the supplied callback
# this is only for urls that are not accessed via ajax
# and should return a view and flash a message
def render_exception(this_template='/index.html', form_callback=False, auth_redirect='project.index'):
    def render_wrapper(f):
        u'''this function creates a wrapper and returns the rendered template for
        create.html if an exception occurs. Or the result if everything works'''
        @wraps(f)
        def trycatch(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception:
                # get exception via handler
                exc_type, exc_instance, exc_traceback = exceptionHandler()
                flash(exc_instance.message, 'bg-danger')
                if isinstance(exc_instance, NotAllowedException):
                    return redirect(url_for(auth_redirect))
                if form_callback is not False:
                    form = form_callback()
                    return render_template(this_template, form=form)
                else:
                    return redirect(url_for(this_template))
        return trycatch
    return render_wrapper

# an exception decorator for ajax functions
def render_js_exception(f):
    u'''this function creates a wrapper and returns the rendered template for
    create.html if an exception occurs. Or the result if everything works'''
    @wraps(f)
    def trycatch(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            # raise the new exception from the instance
            # get exception via handler
            exc_type, exc_instance, exc_traceback = exceptionHandler()
            # raise it so it can be caught by js
            #raise exc_type, exc_instance, exc_traceback
            return exc_instance.message
    return trycatch

def catchDoesNotExist(f):
    @wraps(f)
    def trycatch(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except DoesNotExist:
            return None
    return trycatch

