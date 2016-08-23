import annohub.models.language as language
from mongoengine import DoesNotExist
from mongoengine import NotUniqueError

def get_by_key(language):
    try:
        return language.Language.objects.get(
            key=language
            )
    except DoesNotExist:
        return None

def get_by_id(language_id):
    try:
        return language.Language.objects.get(
            id=language_id
            )
    except DoesNotExist:
        return None


def get_all():
    try:
        return language.Language.objects.order_by('key')
    except DoesNotExist:
        return None

def create(key, name):
    assert isinstance(key, basestring)
    assert isinstance(name, basestring)
    try:
        this_language = language.Language(key, name).save()
        return this_language.id
    except NotUniqueError:
        return None
