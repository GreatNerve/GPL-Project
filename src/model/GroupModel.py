import datetime

from mongoengine import Document, StringField, DateTimeField, ReferenceField

class Group(Document):
    name = StringField(required=True)
    description = StringField(required=False)
    members = ReferenceField('User', required=True)
    created_by = ReferenceField('User', required=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'groups',
        'indexes': [
            'created_by'
        ]
    }

