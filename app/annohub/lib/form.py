# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

u''' these are forms (written LikeThis) and functions to deal with them
(written like_this) '''

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, validators, SelectField, BooleanField
from annohub import app
import annohub.lib.user as user_lib
import annohub.lib.license as license_lib
import annohub.lib.language as language_lib
import annohub.lib.genre as genre_lib
import annohub.lib.tagset as tagset_lib
import annohub.lib.fileutils as fileutils_lib
from flask.ext.wtf.file import FileField, FileRequired

def file_validator(Form):
    #app.logger.debug(request.files['file'].filename)
    #validators.Regexp(re.compile(r'^.+?\.(txt|md|text|rst)$'), re.U, "Only text is supported. Your file has to end with .txt or .md or .text or .rst")
    return True

class Signup(Form):
    username = StringField("Username:", [validators.InputRequired(), validators.Length(min=1, max=50)], description="You have 1 to 50 characters.")
    email = StringField("E-Mail:", [validators.InputRequired(), validators.Email(), validators.Length(min=4, max=50)], description="We won't send you spam. Pinky-promise!")
    password = PasswordField("Password:", [validators.InputRequired(), validators.EqualTo('confirm', message='Passwords must match'), validators.Length(min=6, max=255)], description="You have 6 to 255 characters.")
    confirm = PasswordField("Please type your password again:", [validators.InputRequired()], description="Type it again, please!")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        form_name = self.username.data

        if user_lib._get_by_name(form_name) or \
        (form_name in app.config['USER_BLACKLIST']):
            self.username.errors.append("That name is already taken")
            return False

        if user_lib._get_by_email(self.email.data):
            self.email.errors.append("That email is already taken")
            return False

        return True


class Login(Form):
    username = StringField("Username:", [validators.InputRequired(), validators.Length(min=1, max=50)], description="Let us know who you are!")
    password = PasswordField("Password:", [validators.InputRequired(), validators.Length(min=6, max=255)], description="And proof it, please!")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):

        if not Form.validate(self):
            return False

        if  user_lib.check_password(self.username.data, self.password.data):
            return True
        else:
            self.username.errors.append("Invalid name or password")
            self.password.errors.append("Invalid name or password")
            return False

class CreateProject(Form):

    name = StringField(u"Title:", [validators.InputRequired(), validators.Length(min=1, max=100)], description="How do you want to call this project?")
    language = SelectField(u"Language¹:", [validators.InputRequired()], choices = [ (str(l.id), l.name) for l in language_lib.get_all()])
    genre = SelectField(u"Genre²:", [validators.InputRequired()], choices = [(str(g.id), g.name) for g in genre_lib.get_all()])
    tagset = SelectField(u"Tagset³:", [validators.InputRequired()], choices = [(str(t.id), t.name) for t in tagset_lib.get_all()])
    text = FileField(u"Text File & Preprocessing Options⁴:", [FileRequired()])
    remove_whitespace = BooleanField(u"Remove duplicate whitespace.", [validators.Optional()], default=True)
    join_hyphens = BooleanField(u"Join hyphenated words.", [validators.Optional()], default=True)
    strip_punctuation = BooleanField(u'<span class="glyphicon glyphicon-alert"></span> Strip punctuation', [validators.Optional()], default=False)


    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        return True

class ManageAnnotators(Form):
    username = StringField(u"Annotator:", [validators.InputRequired(), validators.Length(min=1, max=100)], description="Give me the username of one annotator. If you have none, enter your own.")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        form_name = self.username.data
        if not user_lib._get_by_name(form_name) or \
        (form_name in app.config['USER_BLACKLIST']):
            self.username.errors.append("Please enter an existing and valid username.")
            return False
        return True


class ManageAnnotation(Form):
    tagset = SelectField(u"Tagset:", [validators.InputRequired()], choices = [(str(t.id), t.name) for t in tagset_lib.get_all()])
    #name = SelectField(u"Annotator¹:", [validators.InputRequired()], choices = [ (str(u.id), u.name) for u in user_lib.get_all()])
    username = StringField(u"Annotator¹:", [validators.InputRequired(), validators.Length(min=1, max=100)], description="Give me the username of one annotator. If you have none, enter your own.")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        form_name = self.username.data
        if not user_lib._get_by_name(form_name) or \
        (form_name in app.config['USER_BLACKLIST']):
            self.username.errors.append("Please enter an existing and valid username.")
            return False
        return True

class PublishProject(Form):

    license = SelectField(u"License¹:", [validators.InputRequired()], choices = [ (str(l.id), l.name) for l in license_lib.get_all()])
    public = BooleanField(u"Yes, this is a public project!²", [validators.Optional()], default=True)

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        return True

# use libs to get data from the form
def get_name(form):
    this_name = form.data['name']
    assert isinstance(this_name, basestring)
    assert len(this_name) > 0
    return this_name

# use libs to get data from the form
def get_username(form):
    this_name = form.data['username']
    assert isinstance(this_name, basestring)
    assert len(this_name) > 0
    return this_name

def read_text(form):
    return fileutils_lib.read_file(form.data['text'])

def get_language(form):
    #app.logger.debug(form.data['language'])
    return language_lib.get_by_id(form.data['language'])

def get_tagset(form):
    return tagset_lib.get_by_id(form.data['tagset'])

def get_genre(form):
    return genre_lib.get_by_id(form.data['genre'])

def get_public(form):
    if form.data['public']:
        return True
    return False

def get_license(form):
    if form.data['license']:
        return True
    return False
