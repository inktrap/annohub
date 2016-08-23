
from annohub import db

'''
a special class just to save sentences
a sentence has a position and is a list of strings
if token is deleted all the sentences are deleted too
<http://stackoverflow.com/questions/17752597/strategies-for-fast-searches-of-billions-of-small-documents-in-mongodb>
So
SentenceNotTokenized: ST, SU, SA, SUA
'''

class SentenceNotTokenized(db.Document):
    ''' a sentence that has not been tokenized by the user
    but by nltk'''
    # the Token this sentence belongs to
    token_ref = db.ReferenceField('Token')
    # the sentence is a list of strings
    sentence = db.ListField(db.StringField())
    # the position of the sentence in the text
    pos = db.IntField(required=True)

class SentenceTokenized(db.Document):
    ''' a sentence that has been tokenized by nltk and the user'''
    token_ref = db.ReferenceField('Token')
    sentence = db.ListField(db.StringField())
    pos = db.IntField(required=True)

class SentenceNotAnnotated(db.Document):
    ''' a sentence that HAS NOT been annotated by the user
    but by nltk. These will not be deleted because they are default tags!
    for every SentenceTokenized (Token) there is a SentenceNotAnnotated (Tags)
    '''
    token_ref = db.ReferenceField('Token')
    sentence = db.ListField(db.StringField())
    pos = db.IntField(required=True)

class SentenceAnnotated(db.Document):
    ''' a sentence that HAS been annotated by the user
    and by nltk'''
    token_ref = db.ReferenceField('Token')
    annotation_ref = db.ReferenceField('Annotation')
    sentence = db.ListField(db.StringField())
    pos = db.IntField(required=True)

