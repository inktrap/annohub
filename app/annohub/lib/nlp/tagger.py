# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from annohub.lib import error as e
import nltk

class TaggingBackend():
    u''' does the work and tags stuff'''
    def __init__(self, tagset):
        # TODO: if we have taggers that can use more tagsets, this becomes a real option
        self.tagset = tagset
        self.tagset = None

    def main(self, tagger, tokens):
        u''' tag the text here with the configured tagger'''
        assert isinstance(tokens, list)
        assert isinstance(tokens[0], list)
        assert isinstance(tokens[0][0], basestring)
        tagged_text = [ nltk.tag._pos_tag(sentence, self.tagset, tagger) for sentence in tokens ]
        return self.postprocess(tagged_text)

    def postprocess(self, tagged_text):
        u''' split text into lists of tags, token'''
        for index, this_sentence in enumerate(tagged_text):
            # token = []
            tags = []
            for tok, tag in this_sentence:
                # only return the text because the text is stored separately
                # token.append(tok)
                tags.append(tag)
            tagged_text[index] = tags
        # TODO: if we have more maps from the ptb tagset to others, the mapping would happen here
        return tagged_text

class ConfigureTagger():
    u''' configure a tagger via the supplied parameters'''
    def __init__(self, language):
        try:
            # load the nltk tagger (ideally this is a tagger specially trained on the language data)
            # TODO: if taggers are trained on more languages, choosing the correct tagger will happen here
            self.tagger = nltk.tag.perceptron.PerceptronTagger()
        except:
            raise e.NlpTaggerMissing

    def main(self):
        return self.tagger

class Tagger():
    def __init__(self, language, tagset):
        self.tagset = tagset
        self.language = language

    def main(self, this_text):
        assert isinstance(this_text, list)
        configurator = ConfigureTagger(self.language)
        configured_tagger = configurator.main()
        this_tagger = TaggingBackend(self.tagset)
        return this_tagger.main(configured_tagger, this_text)

