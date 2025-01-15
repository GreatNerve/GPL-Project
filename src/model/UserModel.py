import datetime

from mongoengine import Document, StringField, EmailField, DateTimeField, ReferenceField, ListField, UUIDField, \
    ObjectIdField
from src.model.GroupModel import Group

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    clerk_id = StringField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    groups = ListField(ReferenceField('Group'), default=[])
    meta = {
        'collection': 'users',
        'indexes': [
            'email',
            'clerk_id'
        ]
    }
