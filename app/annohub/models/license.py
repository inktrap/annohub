from annohub import db

class License(db.Document):
    u''' language information'''
    key = db.StringField(max_length=20, unique=True)
    name = db.StringField(max_length=150, unique=True)
    url = db.StringField(max_length=200, unique=True)

