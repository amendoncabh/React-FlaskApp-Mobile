from datetime import datetime, UTC
from mongoengine import Document, ObjectIdField, StringField, EmailField, FileField, EmbeddedDocumentField, DateTimeField, BooleanField

from Server.model.commons import LocationAddress
from Server.utils import from_appglobal


class School(Document):
    full_name = StringField(max_length=130, required=True)
    alternative_name = StringField(max_length=20, null=True)

    phone_number = StringField(max_length=15, required=True)
    email = EmailField(null=True)
    address = EmbeddedDocumentField(LocationAddress, required=True)

    enabled = BooleanField(default=True)

    logo = FileField(collection_name='schools', null=True)
    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s (%s)" % (self.name, self.phone_number)

    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(School, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(School, self).update(**kwargs)
