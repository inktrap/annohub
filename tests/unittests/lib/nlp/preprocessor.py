#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
# from base import Base

# make imports work, regardless of the path where this is called from
current_dir=os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(os.path.expanduser(os.path.join(current_dir, '../../../../app/')))
sys.path.append(path)


import annohub.lib.nlp.preprocessor as preprocessor


class TestPreprocessor(unittest.TestCase):

    def test_strip_whitespace(self):
        self.preprocessor = preprocessor.Preprocessor(
            strip_whitespace=True, join_hyphens=False, strip_punctuation=False)
        text = u'''
        This is just  some    text with

        whitespaces
            and tabs.
        '''

        should = u''' This is just some text with whitespaces and tabs. '''

        result = self.preprocessor.strip_whitespace(text)
        if not result == should:
            raise Exception(u'Error: should=%r result=%r' % (
                should, result))

        self.assertEqual(self.preprocessor.main(text),
                         self.preprocessor.strip_whitespace(text))

    def test_join_hyphens(self):
        self.preprocessor = preprocessor.Preprocessor(
            strip_whitespace=False, join_hyphens=True, strip_punctuation=False)
        text = u'''
This is a text with joined-
     This is a text with joined-
This is a text with joined-
a newline and - god know it too notjoined -
some more newlines and dashes in
unicode notjoined-
- said lalalala'''

        should = u'''
This is a text with joinedThis is a text with joinedThis is a text with joineda newline and - god know it too notjoined -
some more newlines and dashes in
unicode notjoined-
- said lalalala'''

        result = self.preprocessor.join_hyphens(text)
        if not result == should:
            raise Exception(u'Error: should=%r result=%r' % (
                should, result))

        self.assertEqual(self.preprocessor.main(text),
                         self.preprocessor.join_hyphens(text))

    def test_strip_punctuation(self):
        self.preprocessor = preprocessor.Preprocessor(
            strip_whitespace=False, join_hyphens=False, strip_punctuation=True)
        text = u'''.asiasjvkf.avaernvkn-vaerfiva- kavdalkfv-adnvlaksv- leave
sentence puncts. ivaorinvoiafm? 23vkflm lks-vam-?!? >foobar« »sentence« and
„some other“ sentence .asiasjvkf.avaernvkn-vaerfiva- kavdalkfv-adnvlaksv- leave
sentence puncts. …ivaorinvoiafm? 23vkflm lks-vam-?!? >foobar« »sentence« and
„some other“ sentence …'''

        should = u'''.asiasjvkf.avaernvkn-vaerfiva kavdalkfv-adnvlaksv leave
sentence puncts. ivaorinvoiafm? 23vkflm lks-vam-?!? foobar sentence and
some other sentence .asiasjvkf.avaernvkn-vaerfiva kavdalkfv-adnvlaksv leave
sentence puncts. …ivaorinvoiafm? 23vkflm lks-vam-?!? foobar sentence and
some other sentence …'''

        result = self.preprocessor.strip_punctuation(text)
        if not result == should:
            raise Exception(u'Error: should=%r result=%r' % (
                should, result))

        self.assertEqual(self.preprocessor.main(text),
                         self.preprocessor.strip_punctuation(text))

        self.preprocessor = preprocessor.Preprocessor(
            strip_whitespace=False, join_hyphens=False, strip_punctuation=True)
        text = u'''
            ~/repository/foobar/barfo/
        ''' * 100

        should = u'''
            repository/foobar/barfo
        ''' * 100

        result = self.preprocessor.strip_punctuation(text)
        if not result == should:
            raise Exception(u'Error: should=%r result=%r' % (
                should, result))

        text = u'''„~/foobrar“'''
        should = u'''foobrar'''

        result = self.preprocessor.strip_punctuation(text)
        if not result == should:
            raise Exception(u'Error: should=%r result=%r' % (
                should, result))


if __name__ == '__main__':
    unittest.main(verbosity=2)
