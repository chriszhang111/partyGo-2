from app import db
import datetime

class User(db.Document):
  name = db.StringField(required=True)
  email = db.StringField(requried=True,unique=True)
  password = db.StringField(requried=True)
  created = db.DateTimeField(default=datetime.datetime.now)
  bio = db.StringField(max_length=200)
  profile_image = db.StringField()
  