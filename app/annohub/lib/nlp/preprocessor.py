# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import re
# import the regex module
import regex as extended_re
from annohub import app

class Preprocessor(object):
    def __init__(self, strip_whitespace=True, join_hyphens=True, strip_punctuation=False):
        self.set_join_hyphens = join_hyphens
        self.set_strip_whitespace = strip_whitespace
        self.set_strip_punctuation = strip_punctuation

        hyphens = [
            45,    # hyphen-minus  the Ascii hyphen, with multiple usage, or “ambiguous semantic value” #; the width should be “average”
            173,   # soft hyphen  “discretionary hyphen”
            1418,  # armenian hyphen  as soft hyphen, but different in shape
            1470,  # hebrew punctuation maqaf  word hyphen in Hebrew
            5120,  # canadian syllabics hyphen  used in Canadian Aboriginal Syllabics
            6150,  # mongolian soft hyphen  as soft hyphen, but displayed at the beginning of the second line
            8208,  # hyphen unambiguously a hyphen character, as in “left-to-right” #; narrow width
            8209,  # non-breaking hyphen  as hyphen (U+2010), but not an allowed line break point
            8722,  # minus sign  an arithmetic operator #; the glyph may look the same as the glyph for a hyphen-minus, or may be longer  #;
            11799, # double oblique hyphen  used in ancient Near-Eastern linguistics #; not in Fraktur, but the glyph of Ascii hyphen or hyphen is similar to this character in Fraktur fonts
            12448, # katakana-hiragana double hyphen in Japasene kana writing
            65123, # small hyphen-minus small variant of Ascii hyphen
            65293, # fullwidth hyphen-minus variant of Ascii hyphen for use with CJK characters 
            ]
        self.hyphens = u''.join([ unichr(i) for i in hyphens ])

        # the list of sentence delimiters that should never be removed,
        # because they can end sentences …
        delimiter_list = ['?', '!', '.', '…']

        # ELLYPSIS
        # ellypsis can mark the end of a sentence, as you noted and are used correctly with a preceeding space
        # they can also mark the end of a word, but I would also not cut them there:
        # f.e. an unfinished 'This' like 'Thi…' looks better than 'Thi'.

        # HYPHENS
        # hyphens have already been joined. this option should not be used if hyphens
        # have not been joined already.

        # make utf8 and escape and then join them
        self.sentence_delimiter = ''.join([extended_re.escape(i.decode('utf-8')) for i in delimiter_list])

    def main(self, this_text):
        if self.set_strip_whitespace:
            this_text = self.strip_whitespace(this_text)
        if self.set_join_hyphens:
            this_text = self.join_hyphens(this_text)
        if self.set_strip_punctuation:
            app.logger.debug("Stripping punctuation")
            this_text = self.strip_punctuation(this_text)

        return this_text

    def strip_whitespace(self, this_text):
        return re.sub(r'\s+', u' ', this_text)

    def strip_punctuation(self, this_text):
        u''' strip punctuation that does not delimit sentences'''
        # regex documentation
        u'''
        ur"                         # beginning of unicode raw regex
        (?V1)                       # specifically use regex-version 1 (this should be a flag!)
        ((?<=\s|^)                  # use a positive lookbehind assertion: this matches if preceeded by a whitespace or the beginning of the file
        ([[[:punct:]]--[{0}]]+))    # an infinite non-empty row of symbols that are in
                                    # the set of punctuation symbols without the set of the delimiter_list
        |                           # this is an or, so we can remove from both ends (just reversing the idea above)
        (([[[:punct:]]--[{0}]]+)    # again, our set, see above
        (?=\s|$))"                  # a lookahead assertion: matches if a space is after the expession before or the file ends

        # and format just moves the excluded delimiters into the right place
        '''
        # create the regex
        this_regex = ur"(?V1)((?<=\s|^)([[[:punct:]]--[{0}]]+))|(([[[:punct:]]--[{0}]]+)(?=\s|$))".format(self.sentence_delimiter)
        return extended_re.sub(this_regex, u'', this_text)

    def join_hyphens(self, this_text):
        u''' join hyphens at the end of a line, that means:
            delete the hypen and remove the linebreak
            - hyphens: <https://www.cs.tut.fi/~jkorpela/dashes.html>
            - find separating hyphens: <https://en.wikipedia.org/wiki/Hyphen#Justification_and_line-wrapping>'''

        u'''
        (?<=\S)     # there has to be a character before the hyphen-
        [-]         # then there is the hyphen: -
        [ \t\f\v]*  # followed by optional whitespace that is not linebreaking
        [\n]+       # then comes the newline or more of them
        [\s]*       # maybe some spaces again, we do not care
        (?=[\w])    # and finally something that is a character or something (ideally all unicode characters).
        '''
        expression = re.compile(r'(?<=\S)[%s][ \t\f\v]*[\n]+[\s]*(?=[\w])' % self.hyphens, re.M | re.U)
        text = re.sub(expression, u'', this_text)

        return text
