#!/usr/bin/env python
# -*- coding: utf-8 -*-
from annohub import app
from annohub.lib import error as e

def try_unicode(this_string, errors='strict'):
    u''' taken from <https://stackoverflow.com/a/9600161>
    and changed so it turns input into unicode
    Attention: Order of ENCODINGS_ALLOWED is important.
    '''
    assert isinstance(this_string, basestring), repr(this_string)
    for enc in app.config['ENCODINGS_ALLOWED']:
        try:
            return unicode(this_string, enc, errors)
        except UnicodeError, exc:
            continue
    raise e.FileutilsInvalidFileEncodingException


def read_file(this_file):
    u''' read the file '''
    try:
        data = this_file.read()
    except IOError:
        raise e.FileutilsInvalidFileReadException
    # stripping unnecessary spaces to test if file is empty
    data = try_unicode(data).strip()

    #app.logger.debug(len(data))
    #app.logger.debug(app.config['SIZE_LIMIT'])

    if len(data) > app.config['SIZE_LIMIT']:
        raise e.FileutilsFileTooLargeException
    elif len(data) > 0:
        return data
    else:
        raise e.FileutilsEmptyFileException
