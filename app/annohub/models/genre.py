from annohub import db

class Genre(db.Document):
    u''' genre information'''
    key = db.StringField(max_length=50, unique=True)
    name = db.StringField(max_length=50, unique=True)

