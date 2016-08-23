# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import nltk
from annohub import app
from annohub.lib import error as e
#import re

class TokenizerBackend():
    def __init__(self,
                sent_tokenize,
                word_tokenize):

        self.sent_tokenize=sent_tokenize
        self.word_tokenize=word_tokenize

    def main(self, this_text):
        u''' alias for the text_to_toks method'''
        return self.text_to_toks(this_text)

    def text_to_toks(self, this_text):
        u''' get sentences and segmentize them into token'''
        assert isinstance(this_text, basestring), repr(this_text)
        return self.sents_to_toks(self.text_to_sents(this_text))

    def text_to_sents(self, this_text):
        u''' get text and segmentize it into sentences, a list of strings'''
        assert isinstance(this_text, basestring), repr(this_text)
        # do not append sentences that are empty
        return [ sent for sent in self.sent_tokenize.tokenize(this_text) if len(sent) > 0 ]

    def sents_to_toks(self, this_sents):
        u''' get a list of sentences as strings and tokenize them. returns list of lists.'''
        assert isinstance(this_sents, list)
        # do not append sentences that contain nothing after the tokenization step (outer list comprehension)
        # take sents:
        # sents ['sentence one is this one', 'this is sentence two']
        # and make this:
        # [['sentence', 'one', 'is', 'this', 'one'], ...]
        # and the tokenization is the output of _sent_to_toks()
        # if a token or a sentence is empty, it won't be appended. (see _sents_to_toks and text_to_sents)
        # if a sentence is empty, because no token was appended, the sentence won't be appended (see this function)
        return [ j for j in [ self._sent_to_toks(sent) for sent in this_sents ] if len(j) > 0 ]

    def _sent_to_toks(self, this_sent):
        u''' get a sentence as a string and tokenize it. returns a list'''
        assert isinstance(this_sent, basestring), repr(this_sent)
        # do not append tokens that are empty or whitespace
        return [ tok for tok in self.word_tokenize.tokenize(this_sent) if len(tok.strip()) > 0 ]

class ConfigureTokenizer():
    def __init__(self, language='english', genre=None):
        self.genre = genre
        self.language = language

    def main(self):

        #app.logger.debug("Getting tokenizer for %s" % self.language)
        word_tokenize = nltk.tokenize.treebank.TreebankWordTokenizer()

        if self.language == app.config['OTHER_LANGUAGE']:
            raise e.NlpSentTokenizerMissing
        try:
            sent_tokenize = nltk.data.load('tokenizers/punkt/%s.pickle' % self.language)
        except Exception as exc:
            app.logger.debug("Language not found (but it should be there!): %s" % self.language)
            app.logger.debug(exc.message)
            raise e.NlpSentTokenizerMissing

        return sent_tokenize, word_tokenize

class Tokenizer():
    def __init__(self, language, genre):
        self.genre = genre
        self.language = language

    def main(self, this_text):
        u'''
             take text and a genre and a language as input.
             do preprocessing
             find the appropriate tokenizer
             return list of list of tokens
        '''

        assert isinstance(this_text, basestring), repr(this_text)

        configurator = ConfigureTokenizer(self.language, self.genre)

        try:
            sent_tokenize, word_tokenize = configurator.main()
        except e.NlpSentTokenizerMissing:
            # either the user has chosen 'other' (which is not bad)
            # or the pickled tokenizers are not available (which is bad)
            app.logger.debug("Falling back to default tokenizer.")
            configurator = ConfigureTokenizer()
            sent_tokenize, word_tokenize = configurator.main()

        tokenize = TokenizerBackend(sent_tokenize, word_tokenize)
        return tokenize.main(this_text)

