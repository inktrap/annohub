import annohub.models.genre as genre
from mongoengine import DoesNotExist
from mongoengine import NotUniqueError

def get_by_key(genre):
    try:
        return genre.Genre.objects.get(
            key=genre
            )
    except DoesNotExist:
        return None

def get_by_id(genre_id):
    try:
        return genre.Genre.objects.get(
            id=genre_id
            )
    except DoesNotExist:
        return None


def get_all():
    try:
        return genre.Genre.objects.order_by('key')
    except DoesNotExist:
        return None

def create(key, name):
    assert isinstance(key, basestring)
    assert isinstance(name, basestring)
    try:
        this_genre = genre.Genre(key, name).save()
        return this_genre.id
    except NotUniqueError:
        return None
