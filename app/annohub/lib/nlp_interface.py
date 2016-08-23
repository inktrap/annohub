
from annohub.lib.nlp import preprocessor, tokenizer, tagger
#from annohub import app

def tokenize_project(file_content, tokenizer_options, preprocessor_options):
    # give all stuff to lib/nlp interface here
    # blueprints coordinate and return exceptions if they fail
    #app.logger.debug("configuring preprocessor")
    this_preprocessor = preprocessor.Preprocessor(preprocessor_options['join_hyphens'], preprocessor_options['strip_whitespace'], preprocessor_options['strip_punctuation'])
    this_text_preprocessed = this_preprocessor.main(file_content)
    #app.logger.debug("preprocessing done")
    this_tokenizer = tokenizer.Tokenizer(tokenizer_options['language'], tokenizer_options['genre'])
    #app.logger.debug("calling tokenizer")
    return this_tokenizer.main(this_text_preprocessed)

def tag_project(text_tokenized, tagger_options):
    # text_tokenized = [["An", "apple", "a", "day", "."], ["Keeps", "the", "doctor", "away", "."]]
    this_tagger = tagger.Tagger(tagger_options['language'], tagger_options['tagset'])
    return this_tagger.main(text_tokenized)
