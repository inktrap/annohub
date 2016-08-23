import annohub.lib.error as e
import annohub.models.project as project_model
from mongoengine import DoesNotExist
#from annohub import app

def get_percent(this_project, this_user):
    this_annotation = get_annotation_by_user(this_project, this_user)
    divisor = float(max(1, this_annotation.annotated + this_annotation.not_annotated))
    percent = (this_annotation.annotated / divisor) * 100
    assert percent <= 100
    assert percent >= 0
    return round(percent, 1)

def get_annotation_by_user(this_project, this_user):
    try:
        annotation = project_model.Annotation.objects.get(project=this_project, user=this_user)
    except DoesNotExist:
        raise
    return annotation

@e.catchDoesNotExist
def _get_annotation_by_user(this_project, this_user):
    return get_annotation_by_user(this_project, this_user)

def get_status(this_project, this_user):
    this_annotation = get_annotation_by_user(this_project, this_user)
    if this_annotation:
        return this_annotation.status

def set_stats(this_project, this_user):
    # sets a projects status to manage
    _set_status(this_project, this_user, index_status('stats'))
    return this_project.id

def _set_status(this_project, this_user, this_status):
    assert isinstance(this_project, project_model.Project)
    assert isinstance(this_status, int)
    annotation = get_annotation_by_user(this_project, this_user)
    # sets a projects status
    annotation.status = this_status
    annotation.save()
    return True

def index_status(status_name):
    assert isinstance(status_name, basestring)

    this_status = ['annotate', 'stats']

    if status_name in this_status:
        return this_status.index(status_name)
    else:
        raise ValueError("%s is is not a valid status. %s" % status_name, ','.join(this_status))

def _delete_annotation(this_project, user):
    u''' delete the annotation of a user. the annotation for the whole project is bound
    to the project and can only be deleted via sentence_lib.delete_all_by_tokenid'''
    this_annotation = _get_annotation_by_user(this_project, user)
    if this_annotation:
        this_annotation.delete()
        return this_project.id

def validate_json(project_id, this_json):
    try:
        this_annotation = this_json['annotation']
        this_id = this_json['id']
        this_token = this_json['token']
    except KeyError:
        raise e.InvalidDataStructure
    if not (this_id == project_id):
        raise e.InvalidDataValues
    return this_token, this_annotation

def validate_annotation(this_token, this_annotation, this_tagset):
    assert isinstance(this_token, list)
    assert isinstance(this_annotation, list)
    assert isinstance(this_tagset, list)
    # number of sentences has to match
    if len(this_token) != len(this_annotation):
        raise e.InvalidDataValues("number of sentences has to match %i is not %i" % ( len(this_token), len(this_annotation)))
    for sentence, tags in enumerate(this_annotation):
        # number of words per sentence has to match
        if len(this_token[sentence]) != len(tags):
            raise e.InvalidDataValues("number of words per sentence has to match")
        # every tag has to be in the tagset
        for tag in tags:
            if tag not in this_tagset:
                raise e.InvalidDataValues("every tag has to be in the tagset")
    return this_annotation

