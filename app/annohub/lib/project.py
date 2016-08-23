#from annohub import app
import annohub.models.project as project_model
import annohub.models.user as user_model
import annohub.lib.sentence as sentence_lib
import annohub.lib.annotation as annotation_lib
import annohub.lib.user as user_lib
import pymongo
import annohub.lib.error as e
from mongoengine import DoesNotExist
import bson

def create(user_id, text_tokenized, name, language, genre, tagset):
    this_token_id = create_token(text_tokenized, len(text_tokenized))
    project_id = create_project(user_id, name, language, genre, tagset, this_token_id)
    this_project = get_project_by_id(project_id)
    this_creator = user_lib.get_by_id(user_id)
    set_creator(this_project, this_creator)
    return this_project.id


def create_project(user_id, name, language, genre, tagset, token_id):
    assert isinstance(user_id, bson.objectid.ObjectId)
    assert isinstance(name, basestring)
    assert isinstance(language, bson.objectid.ObjectId)
    assert isinstance(genre, bson.objectid.ObjectId)
    assert isinstance(tagset, bson.objectid.ObjectId)
    assert isinstance(token_id, bson.objectid.ObjectId)
    try:
        this_project = project_model.Project(creator = user_id,
            language = language,
            genre = genre,
            name = name,
            token = token_id,
            tagset = tagset).save()
        #app.logger.debug("Saved project %s" % this_project.id)
        return this_project.id
    except pymongo.errors.DocumentTooLarge:
        raise e.DocumentTooLarge

def create_token(text_tokenized, num_sentences):
    assert isinstance(text_tokenized, list)
    assert isinstance(text_tokenized[0], list)
    assert isinstance(text_tokenized[0][0], basestring)
    assert isinstance(num_sentences, int)
    try:
        this_token = project_model.Token(not_tokenized = num_sentences, initial_sentences = num_sentences).save()
        #app.logger.debug("Saved token %s" % this_token.id)
    except pymongo.errors.DocumentTooLarge:
        # TODO: bson.errors.DocumentsTooLarge does not exist.
        # see: <http://api.mongodb.org/python/current/api/bson/errors.html>
        # see: <http://api.mongodb.org/python/current/api/pymongo/errors.html>
        raise e.DocumentTooLarge
    sentence_lib.add_not_tokenized_sentences(this_token, text_tokenized)
    return this_token.id

def create_publish(this_project, this_license, this_public):
    # TODO: implement this method
    raise e.NotImplementedFeature
    #return True

def _create_annotation(this_project, this_user):
    u''' the project has been tokenized now the user needs an annotation object'''
    # initialize annotation for user Annotation
    # create untagged sentences SentenceNotAnnotated
    try:
        # we need the value of initial sentences if the project creator skipped tokenization
        if this_project.token.skipped == 1:
            not_annotated_number = this_project.token.initial_sentences
        else:
            not_annotated_number = this_project.token.tokenized
        this_annotation = project_model.Annotation(user = this_user , project = this_project, token = this_project.token, not_annotated = not_annotated_number).save()
    except:
        raise
    return this_annotation.id

def create_annotation(this_project, this_user):
    _create_annotation(this_project, this_user)
    set_annotator(this_project, this_user)
    return True

def get_annotators(project_id):
    this_project = get_project_by_id(project_id)
    if this_project:
        return this_project.annotator

def get_creator(project_id):
    this_project = get_project_by_id(project_id)
    if this_project:
        return this_project.creator

def get_project_by_id(project_id):
    try:
        return project_model.Project.objects.get(id=project_id)
    except DoesNotExist:
        return None

@e.catchDoesNotExist
def _get_token_by_id(token_id):
    return get_token_by_id(token_id)

def get_token_by_id(token_id):
    try:
        return project_model.Token.objects.get(id=token_id)
    except DoesNotExist:
        return None

def _delete_project(this_project, user):
    _delete_token_by_id(this_project.token.id)
    user_lib._unset_creator(this_project, user)
    return this_project.delete()

def _delete_token_by_id(token_id):
    # delete sentences of this project by id
    sentence_lib.delete_all_by_tokenid(token_id)
    this_token = _get_token_by_id(token_id)
    if this_token:
        this_token.delete()

def delete_project_from_creator(project_id, user_id):
    u''' if a creator choses to delete his project '''
    # get all relevant info
    this_annotators = get_annotators(project_id)
    this_creator = get_creator(project_id)
    this_project = get_project_by_id(project_id)

    # check if there is 
    if ((this_creator is not None) and len(this_annotators) == 0):
        _delete_project(this_project, this_creator)
        return True
    elif (len(this_annotators) == 1) and (this_annotators[0].id == this_creator.id):
        annotation_lib.delete(this_project, this_creator)
        _delete_project(this_project, this_creator)
        return True
    return False

def delete_project_from_annotator(project_id, user_id):
    this_project = get_project_by_id(project_id)
    this_user = user_lib.get_by_id(user_id)
    # delete the user from the project
    _project_unset_annotator(this_project, this_user)
    # delete the project from the user
    user_lib._unset_annotator(this_project, this_user)
    # delete the annotation
    annotation_lib._delete_annotation(this_project, this_user)
    return True

def _project_set_creator(this_project, this_user):
    assert isinstance(this_project, project_model.Project)
    assert isinstance(this_user, user_model.User)
    if not this_user.id == this_project.creator:
        this_project.update(creator=this_user)
        this_project.save()
    return this_project.id

def _project_set_annotator(this_project, this_user):
    assert isinstance(this_project, project_model.Project)
    assert isinstance(this_user, user_model.User)
    if not is_annotator(this_project.id, this_user.id):
        this_project.update(push__annotator=this_user)
        this_project.save()
    return this_project.id

def is_annotator(project_id, user_id):
    assert isinstance(project_id, bson.objectid.ObjectId)
    assert isinstance(user_id, bson.objectid.ObjectId)
    return bson.objectid.ObjectId(user_id) in [ this_user.id for this_user in get_annotators(project_id) ]

def set_creator(this_project, this_user):
    assert isinstance(this_project, project_model.Project)
    assert isinstance(this_user, user_model.User)
    user_lib._set_creator(this_project, this_user)
    _project_set_creator(this_project, this_user)
    return True

def set_annotator(this_project, this_user):
    assert isinstance(this_project, project_model.Project)
    assert isinstance(this_user, user_model.User)
    user_lib._set_annotator(this_project, this_user)
    _project_set_annotator(this_project, this_user)
    return True

def _project_unset_annotator(this_project, this_user):
    assert isinstance(this_project, project_model.Project)
    assert isinstance(this_user, user_model.User)
    if is_annotator(this_project.id, this_user.id):
        this_project.update(pull__annotator=this_user)
        this_project.save()
        return this_project.id

def set_annotator_by_name(project_id, name):
    this_user = user_lib.get_by_name(name)
    set_annotator(project_id, this_user)
    return True

def set_manage(this_project):
    # sets a projects status to manage
    _set_status(this_project, index_status('manage'))
    return this_project.id

def set_annotate(this_project):
    # sets a projects status to manage
    _set_status(this_project, index_status('annotate'))
    return this_project.id

#def set_publish(this_project, this_license, this_public):

def set_publish(this_project):
    # sets a projects status to publish
    _set_status(this_project, index_status('publish'))
    return this_project.id

def set_stats(this_project):
    # sets a projects status to manage
    _set_status(this_project, index_status('stats'))
    return this_project.id

def _set_status(project, this_status):
    assert isinstance(project, project_model.Project)
    assert isinstance(this_status, int)
    # sets a projects status
    project.status = this_status
    project.save()
    return True

def get_percent(this_project):
    # get tokenization  percent
    divisor = float(max(1, this_project.token.initial_sentences))
    percent = 100 - ((float(this_project.token.not_tokenized)/divisor) * 100)
    assert percent <= 100
    assert percent >= 0
    return round(percent, 1)

def get_status(this_project):
    # get a projects status
    return this_project.status

def set_tagset(this_project, this_tagset):
    # sets a projects tagset
    this_project.tagset = this_tagset
    this_project.save()
    return this_project.id

def index_status(status_key):
    # gets the index from a status key
    assert isinstance(status_key, basestring)

    this_status = ['tokenize',
        'manage',
        'annotate',
        'publish',
        'stats']

    if status_key in this_status:
        return this_status.index(status_key)
    else:
        raise ValueError("%s is is not a valid status. %s" % status_key, ','.join(this_status))


