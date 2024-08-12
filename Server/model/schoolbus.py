from datetime import datetime, UTC
from mongoengine import Document, ObjectIdField, StringField, IntField, DateTimeField

from Server.model.constants import BUS_STATUS

from Server.utils import from_appglobal


class SchoolBus(Document):
    name = StringField(max_length=30, required=True)
    register = StringField(max_length=10, required=True, unique=True)
    seats = IntField(min_value = 5, max_value = 30, required=True)
    chassis = StringField(max_length=30, null=True)     #TODO: Validação de chassi
    model = StringField(max_length=20, required=True)
    brand = StringField(max_length=20, required=True)

    status = StringField(max_length=1, choices=BUS_STATUS.options, default=BUS_STATUS.default)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s (%s)" % (self.name, self.plate)

    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(SchoolBus, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(SchoolBus, self).update(**kwargs)
