import datetime
from mongoengine import Document, StringField, EmailField, DateTimeField, ReferenceField, ListField, UUIDField, ObjectIdField, FloatField, DictField, BooleanField
from src.model.UserModel import User
import shortuuid
class Travel(Document):
    destination = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    total_budget = FloatField(required=True)
    activities = ListField(StringField(), default=[])
    short_id = StringField(default=lambda: shortuuid.ShortUUID().random(length=9))
    itinerary = ListField(
        DictField(
            fields={
                'day': StringField(required=True),
                "isCompleted": BooleanField(default=False),
                'places': ListField(
                    DictField(
                        fields={
                            'name': StringField(required=True),
                            'category': StringField(),
                            'duration': FloatField(),
                            'visited': BooleanField(default=False),
                            'spent_amount': FloatField()
                        }
                    )
                ),
                'accommodation': DictField(
                    fields={
                        'name': StringField(),
                        'cost': FloatField(),
                        'spent_amount': FloatField(),
                        "isCompleted": BooleanField(default=False)
                    }
                ),
                'mealCost': FloatField(),
                'budget': FloatField(),
                'spent_meal': FloatField(),
                "miscellaneous": FloatField()
            }
        )
    )
    
    created_by = ReferenceField(User, required=True)
    members = ListField(ReferenceField(User), default=[])
    created_at = DateTimeField(default=datetime.datetime.now)
    meta = {
        'collection': 'travels',
    }