from flask import Blueprint
#from annohub import app
from flask import flash, redirect, render_template, url_for
from flask import request
import annohub.lib.user as user_lib
import annohub.lib.form as form_lib
from flask.ext.login import login_user
from flask.ext.login import logout_user, login_required

auth = Blueprint('auth', __name__)

def try_login(name, password):
    if user_lib.check_password(name, password):
        #app.logger.debug("login sucessfull.")
        login_user(user_lib.get_by_name(name))
        flash("Click 'Projects' to work on a project or to create one.", "bg-primary")
    else:
        flash("Login failed.", "bg-warning")
        #app.logger.debug("login failed.")
    return redirect(url_for('index'))

#'rhs menu'
#'if not logged in'
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = form_lib.Login()
    if request.method == 'GET':
        #app.logger.debug("login")
        return render_template('/auth/login.html', form=form)
    elif request.method == 'POST':
        #app.logger.debug("trying login [POST]")
        if form.validate():
            #app.logger.debug("valid [POST]")
            return try_login(form.data['username'], form.data['password'])
        else:
            #app.logger.debug("invalid [POST] from login")
            #app.logger.debug(form.errors)
            return render_template('/auth/login.html', form=form)
    else:
        flash("Unsupported Method.", "bg-warning")
        return redirect(url_for('index'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = form_lib.Signup()
    if request.method == 'GET':
        return render_template('/auth/signup.html', form=form)
    elif request.method == 'POST':
        if form.validate():
            name = form.data['username']
            password = form.data['password']
            user_lib.create_user(name, form.data['email'], password)
            return try_login(name, password)
        else:
            return render_template('/auth/signup.html', form=form)

@auth.route('/reset_password')
def reset_password():
    flash("Password resetting is currently not implemented. Sorry.", "bg-primary")
    return redirect(url_for('index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

