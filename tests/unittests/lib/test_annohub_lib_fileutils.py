#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
# from base import Base

# set environment variable so the right (testing) db is chosen
# compare: <https://github.com/MongoEngine/mongoengine/issues/607>
os.environ['FLASK_ANNOHUB_TESTING'] = '1'

# make imports work, regardless of the path where this is called from
current_dir=os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(os.path.expanduser(os.path.join(current_dir, '../../../app/')))
sys.path.append(path)

from annohub.lib import fileutils

# class TestFileutils(Base):


class TestFileutils(unittest.TestCase):

    def test_try_unicode(self):
        for start, should in [
            ('\xfc', u'ü'),
            ('\xc3\xbc', u'ü'),
            ('\xbb', u'\xbb'),
        ]:
            result = fileutils.try_unicode(start, errors='strict')
            if not result == should:
                raise Exception(u'Error: start=%r should=%r result=%r' % (
                    start, should, result))

os.environ['FLASK_ANNOHUB_TESTING'] = '0'

if __name__ == '__main__':
    unittest.main()
