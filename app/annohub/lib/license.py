import annohub.models.license as license
from mongoengine import DoesNotExist
from mongoengine import NotUniqueError
import urllib2
import json

def get_by_key(license):
    try:
        return license.License.objects.get(
            key=license
            )
    except DoesNotExist:
        return None

def get_by_id(license_id):
    try:
        return license.License.objects.get(
            id=license_id
            )
    except DoesNotExist:
        return None


def get_all():
    try:
        return license.License.objects.order_by('key')
    except DoesNotExist:
        return None

def create(key, name, url):
    assert isinstance(key, basestring)
    assert isinstance(name, basestring)
    assert isinstance(url, basestring)
    try:
        this_license = license.License(key, name, url).save()
        return this_license.id
    except NotUniqueError:
        return None

def get_all_from_github():
    all_licenses_url = "https://api.github.com/licenses"
    req = urllib2.Request(all_licenses_url)
    req.add_header("Accept", "application/vnd.github.drax-preview.raw")
    resp = urllib2.urlopen(req)
    content = resp.read()
    return json.loads(content)

