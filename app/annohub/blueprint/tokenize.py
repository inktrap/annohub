from flask import Blueprint
#from annohub.lib.auth import is_annotator, is_creator, is_annotator_or_creator
from annohub.lib.auth import has_role
import annohub.lib.project as project_lib
import annohub.lib.sentence as sentence_lib
from flask import flash, request, render_template
from flask import redirect, url_for
from annohub import app
import annohub.lib.error as e
import json

tokenize = Blueprint('tokenize', __name__)

''' view '''
@tokenize.route('/<project_id>', methods=['GET'])
@e.render_exception('project.index')
@has_role('creator')
def index(project_id):
    this_project = project_lib.get_project_by_id(project_id)
    if this_project.status <= 1:
        current_text = sentence_lib.get_not_tokenized_sentences(this_project.token)
        return render_template('/tokenize/index.html', project=this_project, text=current_text)
    else:
        raise e.CantTokenize

''' add submit '''
@tokenize.route('/add_sentence/<project_id>', methods=['POST'])
@e.render_js_exception
@has_role('creator')
def add_sentence(project_id):
    app.logger.debug("adding sentence")
    this_json = request.json
    json_keys = this_json.keys()
    #_pretty_print(json_keys)

    if not json_keys[0] == 'token':
        flash("Internal error, invalid format.", "bg-danger")
        app.logger.debug("Internal error, invalid format.")
        raise e.InvalidDataStructure
        #return "Internal error, invalid format."

    return get_sentence(project_id)

@tokenize.route('/skip/<project_id>', methods=['GET'])
@e.render_js_exception
@has_role('creator')
def skip(project_id):
    this_project = project_lib.get_project_by_id(project_id)
    if this_project.token.skipped != 0:
        flash("You already skipped tokenization!", "bg-danger")
        return redirect(url_for('project.index'))
    sentence_lib.skip_tokenization(this_project)
    project_lib.set_manage(this_project)
    flash("You successfully skipped tokenizing!", "bg-success")
    #return json.dumps("Skipped Tokenization!")
    return redirect(url_for('project.index'))

@tokenize.route('/submit/<project_id>', methods=['POST'])
@e.render_js_exception
@has_role('creator')
def submit(project_id):
    this_project = project_lib.get_project_by_id(project_id)
    this_json = request.json
    json_keys = this_json.keys()
    if not  (json_keys[0] == 'token') and (len(json_keys) == 2):
        app.logger.debug('key error')
        raise e.InvalidDataStructure
    insert_submit(project_id, this_json['token'])
    current_text = sentence_lib.get_not_tokenized_sentences(this_project.token)
    if len(current_text) == 0: # and (this_project.token.not_tokenized == 0):
        project_lib.set_manage(this_project)
        flash("You finished tokenizing your project! Congratulations!", "bg-success")
        return "EOF";
    else:
        return json.dumps(current_text)

def get_sentence(project_id):
    #u''' add another sentence to the current tokenizing session'''
    this_token = project_lib.get_project_by_id(project_id).token
    this_sentence = sentence_lib.get_not_tokenized_sentence(this_token)
    if this_sentence:
        return json.dumps(this_sentence)
    else:
        return "EOF"

def insert_submit(project_id, token):
    this_project = project_lib.get_project_by_id(project_id)
    if len(token) > 0:
        sentence_lib.add_tokenized_sentences(this_project.token, token)
        this_project.token.modify(additional=0)
        this_project.token.save()
    return this_project.token.id

