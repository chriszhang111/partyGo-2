from app import db
from user.models import User


class Party(db.Document):
  name = db.StringField(required=True)
  place = db.StringField(required=True)
  location = db.PointField(required=True)
  start_time = db.DateTimeField(required=True)
  end_time = db.DateTimeField(required=True)
  party_photo = db.StringField()
  description = db.StringField(min_length=20,required=True)
  host = db.ObjectIdField(required=True)
  cancel = db.BooleanField(default=False)
  attendees = db.ListField(db.ReferenceField(User))