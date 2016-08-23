from flask import Blueprint
#from annohub.lib.auth import is_annotator, is_creator, is_annotator_or_creator
from annohub.lib.auth import has_role
import annohub.lib.project as project_lib
import annohub.lib.sentence as sentence_lib
import annohub.lib.annotation as annotation_lib
import annohub.lib.tagset as tagset_lib
from flask import flash, render_template
#from flask import request
import annohub.lib.user as user_lib
from flask.ext.login import current_user
from flask import redirect, url_for
from annohub import app
import annohub.lib.error as e
import json
import operator
from flask import request

annotate = Blueprint('annotate', __name__)

''' view '''
@annotate.route('/<project_id>', methods=['GET'])
@e.render_exception('project.index')
@has_role('annotator')
def index(project_id):
    this_project = project_lib.get_project_by_id(project_id)
    if this_project.status == project_lib.index_status('annotate'):
        this_user = user_lib.get_by_id(current_user.id)
        if this_user:
            this_annotation = annotation_lib.get_annotation_by_user(this_project, this_user)
            if this_annotation.skipped == 1:
                raise e.CantAnnotate('You already skipped annotation!')
            if this_annotation.status != annotation_lib.index_status('annotate'):
                raise e.CantAnnotate('You already annotated this project!')
            if this_annotation.not_annotated < 1:
                raise e.CantAnnotate('There are no sentences left to annotate')
            current_annotation, current_token = sentence_lib.get_not_annotated_sentences(this_annotation)
            tags = sorted_tagset('key', 'key', tagset_lib.get_by_id(this_project.tagset.id))
            return render_template('/annotate/index.html', project=this_project, annotation=current_annotation, token=current_token, tags=tags)
    else:
        raise e.CantAnnotate()

@annotate.route('/skip/<project_id>', methods=['GET'])
@e.render_js_exception
@has_role('creator')
def skip(project_id):
    this_project = project_lib.get_project_by_id(project_id)
    this_user = user_lib.get_by_id(current_user.id)
    this_annotation = annotation_lib.get_annotation_by_user(this_project, this_user)
    if this_annotation.skipped != 0:
        flash("You already skipped tagging!", "bg-danger")
        return redirect(url_for('project.index'))
    sentence_lib.skip_annotation(this_project, this_annotation)
    project_lib.set_stats(this_project)
    flash("You successfully skipped tagging!", "bg-success")
    #return json.dumps("Skipped Tokenization!")
    return redirect(url_for('project.index'))

#@e.render_js_exception
@annotate.route('/submit/<project_id>', methods=['POST'])
@has_role('annotator')
def submit(project_id):
    # get info
    this_project = project_lib.get_project_by_id(project_id)
    this_user = user_lib.get_by_id(current_user.id)
    this_json = request.json
    user_annotation = annotation_lib.get_annotation_by_user(this_project, this_user)
    # check if annotation is still possible
    if user_annotation.skipped == 1:
        raise e.CantAnnotate('You already skipped annotation!')
    if user_annotation.status != annotation_lib.index_status('annotate'):
        raise e.CantAnnotate('You already annotated this project!')
    if user_annotation.not_annotated <1:
        raise e.CantAnnotate('There are no sentences left to annotate')
    # validate annotation
    this_token, this_annotation = annotation_lib.validate_json(project_id, this_json)
    this_tagset = tagset_lib.get_keys_by_id(this_project.tagset.id)
    valid_annotation = annotation_lib.validate_annotation(this_token, this_annotation, this_tagset)
    if len(valid_annotation) > user_annotation.not_annotated:
        raise e.InvalidDataStructure('You are trying to save more sentences than the sentences that are left.')
    # save annotation
    sentence_lib.add_annotated_sentences(user_annotation, valid_annotation)
    # increment annotated counter
    user_annotation.not_annotated -= len(valid_annotation)
    user_annotation.annotated += len(valid_annotation)
    user_annotation.save()
    # get new sentences to annotate, or annotation is finished
    if user_annotation.not_annotated > 0:
        current_annotation, current_token = sentence_lib.get_not_annotated_sentences(user_annotation)
        return json.dumps({'annotation': current_annotation, 'token': current_token})
    else:
        annotation_lib.set_stats(this_project, this_user)
        flash("You finished annotation!", "bg-success")
        return "EOF"

def sorted_tagset(key, by, tagset):
    # TODO: implement sort by most frequent key
    this_tagset = tagset.entries
    sorted_tagset = False
    #result = dict()
    if key == 'key':
        if by == 'key':
            sorted_tagset = sorted(this_tagset, key=operator.attrgetter('key'))
    if sorted_tagset is False:
        raise e.NotImplementedFeature("Sorting by something else than key is not implemented.")
    #for i in sorted_tagset:
    #    result[i['key']] = {'example':i['example'], 'description':i['description']}
    return sorted_tagset
