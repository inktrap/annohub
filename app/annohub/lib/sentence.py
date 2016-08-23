import annohub.models.sentence as sentence_model
import annohub.models.project as project_model
from annohub import app
import annohub.lib.error as e

def add_not_tokenized_sentences(this_token, text_tokenized):
    for index, this_sent in enumerate(text_tokenized):
        # TODO: rollback if saving for not tokenized sentences fail
        # TODO: what happens with malformed content?
        try:
            add_not_tokenized_sentence(this_token, this_sent, index)
        except Exception as exc:
            #_delete_tokens_by_projectid(this_token.id)
            raise exc

def remove_not_tokenized_sentences(this_token):
    this_sentences = sentence_model.SentenceNotTokenized.objects(token_ref=this_token.id).order_by('pos').limit(app.config['SENTENCE_LIMIT'] + this_token.additional).delete()
    this_token.not_tokenized -= this_sentences
    this_token.save()
    return this_sentences

def add_tokenized_sentences(this_token, text_tokenized):
    for index, this_sent in enumerate(text_tokenized):
        # TODO: rollback if saving for not tokenized sentences fail
        # TODO: what happens with malformed content?
        try:
            add_tokenized_sentence(this_token, this_sent, this_token.tokenized + index)
        except Exception as exc:
            #_delete_tokens_by_projectid(this_token.id)
            raise exc
    remove_not_tokenized_sentences(this_token)
    this_token.tokenized += index + 1
    this_token.save()
    return this_token.id

def add_not_tokenized_sentence(token_ref, this_sentence, pos):
    return sentence_model.SentenceNotTokenized(token_ref=token_ref, sentence=this_sentence, pos=pos).save().id

# TODO: add the tokenized sentences and incement the pos field
def add_tokenized_sentence(token_ref, this_sentence, pos):
    return sentence_model.SentenceTokenized(token_ref=token_ref, sentence=this_sentence, pos=pos).save().id

def add_not_annotated_sentences(this_project, this_sentences):
    assert len(this_sentences) > 0
    assert isinstance(this_sentences, list)
    assert isinstance(this_sentences[0], list)
    assert isinstance(this_sentences[0][0], basestring)
    assert isinstance(this_project, project_model.Project)
    sentences = []
    for index, this_sent in enumerate(this_sentences):
        sentences.append(sentence_model.SentenceNotAnnotated(token_ref=this_project.token.id, sentence=this_sent, pos=index))
    sentence_model.SentenceNotAnnotated.objects.insert(sentences)
    return True

def add_annotated_sentences(this_annotation, this_sentences):
    assert len(this_sentences) > 0
    assert isinstance(this_sentences, list)
    assert isinstance(this_sentences[0], list)
    assert isinstance(this_sentences[0][0], basestring)
    assert isinstance(this_annotation, project_model.Annotation)
    sentences = []
    for index, this_sent in enumerate(this_sentences):
        sentences.append(sentence_model.SentenceAnnotated(annotation_ref=this_annotation, token_ref=this_annotation.token, sentence=this_sent, pos=index + this_annotation.annotated + 1))
    sentence_model.SentenceAnnotated.objects.insert(sentences)
    return True


def get_not_tokenized_sentences(this_token, this_limit=app.config['SENTENCE_LIMIT']):
    this_sentences = sentence_model.SentenceNotTokenized.objects(token_ref=this_token.id).order_by('pos').limit(this_limit + this_token.additional).only('sentence')
    return [ this_sentence.sentence for this_sentence in this_sentences ]

def get_all_tokenized_sentences(this_token):
    this_sentences = sentence_model.SentenceTokenized.objects(token_ref=this_token.id).order_by('pos').only('sentence')
    return [ this_sentence.sentence for this_sentence in this_sentences ]


# get tokenized sentences and notannotated sentences at once
# check if their counts are equal
# both indices depend on the annotation object of the user
# return both at the same time
def get_not_annotated_sentences(annotation, this_limit=app.config['SENTENCE_LIMIT']):
    if annotation.not_annotated <1:
        raise e.CantAnnotate
    this_sentences = sentence_model.SentenceTokenized.objects(token_ref=annotation.token.id).order_by('pos').skip(annotation.annotated).limit(this_limit).only('sentence')
    this_annotations = sentence_model.SentenceNotAnnotated.objects(token_ref=annotation.token.id).order_by('pos').skip(annotation.annotated).limit(this_limit).only('sentence')
    text = [ this_sentence.sentence for this_sentence in this_sentences ]
    annotation = [ this_annotation.sentence for this_annotation in this_annotations ]
    return annotation, text

def skip_tokenization(this_project):
    this_token = this_project.token
    if this_token.not_tokenized == 0:
        return this_token.id
    this_sentences = sentence_model.SentenceNotTokenized.objects(token_ref=this_token.id).order_by('pos').only('sentence')
    if this_sentences:
        #this_token.tokenized = len(this_sentences)
        #this_token.not_tokenized = 0
        this_token.skipped = 1
        this_token.save()
        sentences = []
        for index, this_sent in enumerate(this_sentences):
            sentences.append(sentence_model.SentenceTokenized(token_ref=this_token.id, sentence=this_sent.sentence, pos=index))
        sentence_model.SentenceTokenized.objects.insert(sentences)
        this_sentences = sentence_model.SentenceNotTokenized.objects(token_ref=this_token.id).order_by('pos').delete()
    return this_token.id

def skip_annotation(this_project, this_annotation):
    # TODO test this
    this_sentences = sentence_model.SentenceNotAnnotated.objects(token_ref=this_project.token.id).order_by('pos').skip(this_annotation.annotated).only('sentence')
    sentences = []
    for index, this_sent in enumerate(this_sentences):
        sentences.append(sentence_model.SentenceAnnotated(annotation_ref=this_annotation, token_ref=this_project.token.id, sentence=this_sent.sentence, pos=index + this_annotation.annotated + 1))
    sentence_model.SentenceAnnotated.objects.insert(sentences)
    #this_annotation.not_annotated = 0
    this_annotation.skipped = 1
    this_annotation.save()
    return this_project.token.id

def get_not_tokenized_sentence(this_token):
    this_sentences = sentence_model.SentenceNotTokenized.objects(token_ref=this_token.id).order_by('pos').skip(app.config['SENTENCE_LIMIT'] + this_token.additional).limit(1).only('sentence')
    if this_sentences:
        this_token.additional += 1
        this_token.save()
    return [ this_sentence.sentence for this_sentence in this_sentences ]

def delete_all_by_tokenid(token_ref):
    # TODO: test
    try:
        this_untok = sentence_model.SentenceTokenized.objects(token_ref=token_ref)
        if this_untok:
            this_untok.delete()
        this_tok = sentence_model.SentenceNotTokenized.objects(token_ref=token_ref)
        if this_tok:
            this_tok.delete()
        this_unann = sentence_model.SentenceNotAnnotated.objects(token_ref=token_ref)
        if this_unann:
            this_unann.delete()
    except Exception as exc:
        raise exc

