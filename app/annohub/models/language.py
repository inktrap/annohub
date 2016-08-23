from annohub import db

class Language(db.Document):
    u''' language information'''
    key = db.StringField(max_length=50, unique=True)
    name = db.StringField(max_length=50, unique=True)

