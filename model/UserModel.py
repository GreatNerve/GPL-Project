import datetime

from mongoengine import Document, StringField, EmailField, DateTimeField, ReferenceField, ListField, UUIDField, \
    ObjectIdField
from model.GroupModel import Group

class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    user_app_write_id = UUIDField(required=True,unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    groups = ListField(ReferenceField('Group'), default=[])

    meta = {
        'collection': 'users',
        'indexes': [
            'email',
            'user_app_write_id'
        ]
    }
