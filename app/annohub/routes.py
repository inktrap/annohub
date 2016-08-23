# -*- coding: utf-8 -*-
from annohub import app
from flask import flash, render_template, abort, redirect, url_for
#from flask import request, session
from annohub.lib.db import Db as DbImport
import annohub.lib.user as user
from annohub import login_manager
#from bson import DocumentTooLarge

# flash can take the following properties:
# bg-primary
# bg-success
# bg-info
# bg-warning
# bg-danger

import datetime
now = datetime.datetime.now()

@login_manager.user_loader
def load_user(name):
    return user._get_by_name(name)

@login_manager.unauthorized_handler
def unauthorized():
    flash('Please log in.', "bg-warning")
    return redirect(url_for('auth.login'))

@app.errorhandler(404)
def page_not_found(e):
    err = {
        'code':404,
        'message':"page not found",
        'desc':"We are sorry, but the page you are looking for could not be found."
    }
    return render_template('error.html', err=err), err['code']

@app.errorhandler(403)
def page_not_allowed(e):
    err = {
        'code':403,
        'message':"permission denied",
        'desc':"Please authenticate yourself if you want to view this page."
    }
    return render_template('error.html', err=err), err['code']

@app.errorhandler(405)
def method_not_allowed(e):
    err = {
        'code':405,
        'message':"method not allowed",
        'desc':"The method you used is not allowed."
    }
    return render_template('error.html', err=err), err['code']

@app.errorhandler(500)
def internal_server_error(e):
    err = {
        'code':500,
        'message':"internal server error",
        'desc':"We are sorry, but the server has internal problems."
    }
    return render_template('error.html', err=err), err['code']

@app.route(app.config['RESET_DB_URL'])
def reset(secret_token=None):
    if secret_token == app.config['SECRET_RESET_DB_TOKEN']:
        this_dbi = DbImport()
        this_dbi.reset()
        flash('Reset was successfull.', 'bg-success')
        return redirect(url_for('index'))
    else:
        abort(403)

@app.route(app.config['SETUP_DB_URL'])
def setup(secret_token=None):
    if secret_token == app.config['SECRET_SETUP_DB_TOKEN']:
        this_dbi = DbImport()
        this_dbi.setup()
        flash('Setup was successfull. Restart the application.', 'bg-warning')
        return redirect(url_for('index'))
    else:
        abort(403)

@app.route(app.config['UPDATE_NLTK_URL'])
def update(secret_token=None):
    if secret_token == app.config['SECRET_NLTK_TOKEN']:
        this_dbi = DbImport()
        this_dbi._nltk_setup()
        flash('Update was successfull.', 'bg-success')
        return redirect(url_for('index'))
    else:
        abort(403)
