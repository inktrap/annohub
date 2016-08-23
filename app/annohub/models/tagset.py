from annohub import db

class Tag(db.EmbeddedDocument):
    u''' an entry in a tagset'''
    key = db.StringField()
    description = db.StringField()
    example = db.StringField()

class Tagsets(db.Document):
    u''' language information'''
    key = db.StringField(max_length=50, unique=True)
    name = db.StringField(max_length=50, unique=True)
    # embedded tagset documents (the entries) here
    entries = db.ListField(db.EmbeddedDocumentField(Tag))
