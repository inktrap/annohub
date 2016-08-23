from flask import Blueprint
from annohub import app
from flask import flash, redirect, render_template, url_for

page = Blueprint('page', __name__)
@page.route('/tryout')
def tryout():
    flash("Log in as user '%s' with password '%s'" % \
        (app.config['DEFAULT_USER'], app.config['DEFAULT_USER']), "bg-primary")
    return redirect(url_for('auth.login'))

@page.route('/imprint')
def imprint():
    return render_template('/page/imprint.html')

@page.route('/privacy')
def privacy():
    return render_template('/page/privacy.html')

@page.route('/github')
def github():
    return redirect(app.config['GITHUB'])

@page.route('/docs')
def docs():
    return render_template('/page/docs.html')

@app.route('/')
def index():
    flash("If you are new here, why don't you read the Documentation or Tryout annohub?", "bg-primary")
    return render_template('/page/index.html')

