from flask import Blueprint
from flask import flash, request, redirect, render_template, url_for
from annohub.lib.auth import has_role
import annohub.lib.form as form_lib
import annohub.lib.project as project_lib
import annohub.lib.annotation as annotation_lib
import annohub.lib.user as user_lib
import annohub.lib.nlp_interface as nlp_interface
import annohub.lib.error as e
from flask.ext.login import login_required, current_user
#from annohub import app

project = Blueprint('project', __name__)

@project.route('/')
@login_required
def index():
    #app.logger.debug("Showing projects")
    this_user = user_lib.get_by_name(current_user.name).id

    u''' default action returns a list of unstarted projects'''
    #if request.method == 'GET':
    to_tokenize = user_lib.get_all_by_creator(this_user)
    for this_project in to_tokenize:
        setattr(this_project, 'percent', project_lib.get_percent(this_project))
        setattr(this_project, 'status', project_lib.get_status(this_project))
    to_annotate = user_lib.get_all_by_annotator(this_user)
    #app.logger.debug(to_annotate)
    for this_project in to_annotate:
        setattr(this_project, 'percent', annotation_lib.get_percent(this_project, this_user))
        setattr(this_project, 'status', annotation_lib.get_status(this_project, this_user))
        setattr(this_project, 'tagset', this_project.tagset)
    return render_template('/project/index.html', tokenization_projects=to_tokenize, annotation_projects=to_annotate)

@project.route('/create', methods=['GET', 'POST'])
@project.route('/create/', methods=['GET', 'POST'])
@e.render_exception('/project/create.html', form_callback=form_lib.CreateProject, auth_redirect='auth.login')
@login_required
def create():
    form = form_lib.CreateProject()
    if request.method == 'GET':
        # this is a sample test that shows how a function (raiseError) works
        # when it raises an exception and is decorated with render_exception
        #return raiseError(ValueError, "This is a value error")
        return render_template('/project/create.html', form=form)
    elif request.method == 'POST':
        return create_project(form)

@project.route('/export/<project_id>')
@project.route('/export/<project_id>/')
@e.render_exception('project.index')
@has_role('creator')
def export(project_id):
    raise e.NotImplementedFeature
    return "Export"

@project.route('/stats/<project_id>', methods=['GET'])
@project.route('/stats/<project_id>/', methods=['GET'])
@e.render_exception('project.index')
@has_role('creator')
def stats(project_id):
    raise e.NotImplementedFeature
    return "Stats"

@project.route('/transfer/<project_id>')
@project.route('/transfer/<project_id>/')
@e.render_exception('project.index')
@has_role('creator')
def transfer(project_id):
    raise e.NotImplementedFeature
    return "Transfer"

@project.route('/publish/<project_id>', methods=['GET', 'POST'])
@project.route('/publish/<project_id>/', methods=['GET', 'POST'])
@e.render_exception('/project/publish.html', \
        form_callback=form_lib.PublishProject, \
        auth_redirect='project.index')
@has_role('creator')
def publish(project_id):
    this_project = project_lib.get_project_by_id(project_id)
    # TODO check that the annotators finished annotating
    # this has to happen when every annotator finishes or skips tagging
    # (check all annotators so the status can be set to publish if they are done)
    # percentage needs to be checked for manage annotators also
    if project_lib.get_status(this_project) != project_lib.index_status('publish'):
         e.NotAllowedException("Your annotators need to finish annotating this project first")
    form = form_lib.PublishProject()
    if request.method == 'GET':
        return render_template('/project/publish.html', project_id=project_id, form=form)
    elif request.method == 'POST':
        project_lib.set_stats(this_project)
        return create_publish(project_id, form)

def create_publish(project_id, form):
    if form.validate():
        this_license = form_lib.get_license(form)
        this_public = form_lib.get_public(form)
        this_project = project_lib.get_project_by_id(project_id)
        if project_lib.create_publish(this_project, this_license, this_public):
            # TODO: check if annotators finished and *then* set status
            project_lib.set_publish(this_project)
            flash('Now your project has a license and a privacy status.', 'bg-success')
            return redirect(url_for('project.index'))
        else:
            flash('Could not publish your project', 'bg-error')
            return redirect(url_for('project.index'))
    else:
        #app.logger.debug("form did not validate")
        return render_template('/project/publish.html', project_id=project_id, form=form)

def create_project(form):
    u''' this is the create_project method of lib
    it will call the the create_project function from the project model
    and is only here to get the data from the form
    '''

    if form.validate():
        tokenizer_options = {}
        # validate the form and get all the content from the fields
        file_content = form_lib.read_text(form)
        this_name = form_lib.get_name(form)
        this_language = form_lib.get_language(form)
        this_genre = form_lib.get_genre(form)
        tokenizer_options['language'] = this_language.key
        tokenizer_options['genre'] = this_genre.key
        this_tagset = form_lib.get_tagset(form)
        this_text_tokenized = call_tokenize(file_content, tokenizer_options, form)
        #app.logger.debug("tokenizing was successfull")

        # the wrapper only exists so exceptions for project creation can
        # be returned to the user by the decorator
        this_project = project_lib.create(
            user_id = current_user.id,
            text_tokenized = this_text_tokenized,
            name = this_name,
            language = this_language.id,
            genre = this_genre.id,
            tagset = this_tagset.id
            )
        if this_project:
            flash("Tokenization and upload was successfull.", "bg-success")
        return redirect(url_for('project.index'))
    else:
        #app.logger.debug("form did not validate")
        return render_template('/project/create.html', form=form)

# call the tokenizer
def call_tokenize(file_content, tokenizer_options, form):
    preprocessor_options = {}
    #app.logger.debug("starting tokenizing")

    # initialize as False
    strip_whitespace = False
    strip_punctuation = False
    join_hyphens = False

    try:
        if form.data['strip_whitespace']:
            strip_whitespace = True
    except KeyError:
        pass
    try:
        if form.data['strip_punctuation']:
            strip_punctuation = True
    except KeyError:
        pass
    try:
        if form.data['join_hyphens']:
            join_hyphens = True
    except KeyError:
        pass

    preprocessor_options['join_hyphens'] = join_hyphens
    preprocessor_options['strip_whitespace'] = strip_whitespace
    preprocessor_options['strip_punctuation'] = strip_punctuation

    return nlp_interface.tokenize_project(file_content, tokenizer_options, preprocessor_options)

