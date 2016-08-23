from flask import Blueprint
from flask import flash, request, redirect, render_template, url_for
from annohub.lib.auth import has_role
import annohub.lib.project as project_lib
import annohub.lib.nlp_interface as nlp_interface
import annohub.lib.sentence as sentence_lib
import annohub.lib.error as e
from flask.ext.login import current_user
import annohub.lib.form as form_lib
import annohub.lib.user as user_lib
#import json
#import sys

manage = Blueprint('manage', __name__)

@manage.route('/annotation/<project_id>', methods=['GET', 'POST'])
@manage.route('/annotation/<project_id>/', methods=['GET', 'POST'])
@e.render_exception('project.index')
@has_role('creator')
def annotation(project_id):
    this_project = project_lib.get_project_by_id(project_id)
    this_status = project_lib.get_status(this_project)
    if this_status < project_lib.index_status('manage'):
        flash('You have to finish tokenization (or skip it) before you can start tagging.', 'bg-error')
        return redirect(url_for('project.index'))
    elif this_status > project_lib.index_status('manage'):
        flash('We already tagged your project. If you want to manage annotators, use the menu on the left.', 'bg-error')
        return redirect(url_for('project.index'))
    form = form_lib.ManageAnnotation()
    if request.method == 'GET':
        return render_template('manage/annotation.html', form=form, project_id=project_id)
    elif request.method == 'POST':
        return call_tag(this_project, form)

@manage.route('/add/<project_id>', methods=['POST'])
@manage.route('/add/<project_id>/', methods=['POST'])
@e.render_exception('project.index')
@has_role('creator')
def add(project_id):
    this_project = project_lib.get_project_by_id(project_id)
    this_status = project_lib.get_status(this_project)
    if this_status < project_lib.index_status('manage'):
        flash('You have to finish tokenization before you can manage annotators.', 'bg-error')
        return redirect(url_for('project.index'))
    form = form_lib.ManageAnnotators()
    if _add_annotator(this_project, form):
        flash('Now your new annotator can start annotating!', 'bg-success')
        return redirect(url_for('manage.index', project_id=project_id))
    else:
        #app.logger.debug("form did not validate")
        return redirect(url_for('manage.index', project_id=project_id))

@manage.route('/remove/<project_id>/<user_id>', methods=['GET'])
@manage.route('/remove/<project_id>/<user_id>/', methods=['GET'])
@e.render_exception('project.index')
@has_role('creator')
def remove(project_id, user_id):
    ret = annotator_delete(project_id=project_id, user_id=user_id)
    if ret:
        flash("Annotator removed successfully.", "bg-success")
    else:
        flash("Can not remove annotator.", "bg-danger")
    return redirect(url_for('manage.index', project_id=project_id))

@manage.route('/<project_id>', methods=['GET'])
@manage.route('/<project_id>/', methods=['GET'])
@e.render_exception('project.index')
@has_role('creator')
def index(project_id):
    this_project = project_lib.get_project_by_id(project_id)
    this_status = project_lib.get_status(this_project)
    this_annotators = project_lib.get_annotators(this_project.id)
    if this_status < project_lib.index_status('manage'):
        flash('You have to finish tokenization before you can manage annotators.', 'bg-error')
        return redirect(url_for('project.index'))
    form = form_lib.ManageAnnotators()
    return render_template('manage/index.html', form=form, project_id=project_id, this_annotators=this_annotators)

@e.render_exception('project.index')
@has_role('annotator')
def annotator_delete(project_id, user_id):
    return project_lib.delete_project_from_annotator(project_id, user_id)

@e.render_exception('project.index')
@has_role('creator')
def creator_delete(project_id, user_id):
    return project_lib.delete_project_from_creator(project_id, user_id)

@e.render_exception('project.index')
@has_role('creator')
@manage.route('/delete/<role>/<project_id>')
@manage.route('/delete/<role>/<project_id>/')
def delete(role, project_id):
    user_id = current_user.id
    if role == 'creator':
        u'''delete route that is used by a creator'''
        ret = creator_delete(project_id=project_id, user_id=user_id)
    elif role == 'annotator':
        ret = annotator_delete(project_id=project_id, user_id=user_id)

    if ret and role == 'creator':
        flash("Project deleted successfully.", "bg-success")
    elif ret and role == 'annotator':
        flash("You quit.", "bg-success")
    else:
        flash("There has been an error", "bg-danger")

    return redirect(url_for('project.index'))

def _add_annotator(this_project, form):
    if form.validate():
        this_name = form_lib.get_username(form)
        this_annotator = user_lib.get_by_name(this_name)
        if project_lib.is_annotator(this_project.id, this_annotator.id):
            raise e.CantCompleteAction("This user is already an annotator for this project")
        # create annotation object for annotator
        project_lib.create_annotation(this_project, this_annotator)
        return True
    else:
        return False

def call_tag(this_project, form):
    u''' this function is like the call_tokenize function of the project
    blueprint and calls the nlp_interface.tag_project() function'''
    if form.validate():
        # get annotator. annotator is set by create_annotation()
        this_annotator = form_lib.get_username(form)
        this_annotator = user_lib.get_by_name(this_annotator)
        #tagger_options = {'language': this_project.language.name, 'tagset' : form_lib.get_tagset(form)}
        tagger_options = {'language': this_project.language.name, 'tagset' : form_lib.get_tagset(form)}
        project_lib.set_tagset(this_project, tagger_options['tagset'])
        text_tokenized = sentence_lib.get_all_tokenized_sentences(this_project.token)
        default_annotation = nlp_interface.tag_project(text_tokenized, tagger_options)
        # create untagged sentences (this means: untagged by the user!!!) SentenceNotAnnotated
        sentence_lib.add_not_annotated_sentences(this_project, default_annotation)
        # initialize annotation for user Annotation
        project_lib.create_annotation(this_project, this_annotator)
        flash('We tagged your project and your new annotator can start.', 'bg-success')
        # change the status of the project to annotate
        project_lib.set_annotate(this_project)
        return redirect(url_for('project.index'))
    else:
        #app.logger.debug("form did not validate")
        return render_template('/manage/index.html', project_id=this_project.id, form=form)
