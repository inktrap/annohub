import annohub.models.tagset as tagset
from mongoengine import DoesNotExist
from mongoengine import NotUniqueError
#from annohub import app

def get_by_key(tagset):
    try:
        return tagset.Tagsets.objects.get(
            key=tagset
            )
    except DoesNotExist:
        return None

def get_by_id(tagset_id):
    try:
        return tagset.Tagsets.objects.get(
            id=tagset_id
            )
    except DoesNotExist:
        return None

def get_keys_by_id(tagset_id):
    try:
        return [ tag.key for tag in get_by_id(tagset_id).entries ]
    except AttributeError:
        return None

def get_all():
    try:
        return tagset.Tagsets.objects.order_by('key')
    except DoesNotExist:
        return None

def create(key, name, this_tagset):
    assert isinstance(key, basestring)
    assert isinstance(name, basestring)
    assert isinstance(this_tagset, dict)
    try:
        this_tagsets = tagset.Tagsets(key, name).save()
    except NotUniqueError:
        return None
    for tag, entry in this_tagset.items():
        #app.logger.debug("Tag: " + tag)
        #app.logger.debug("Description: " + entry[0])
        #app.logger.debug("Example: " + entry[1])
        tagset_entry = tagset.Tag(key=tag, description=entry[0], example=entry[1])
        this_tagsets.entries.append(tagset_entry)
    this_tagsets.save()
    return this_tagsets.id
