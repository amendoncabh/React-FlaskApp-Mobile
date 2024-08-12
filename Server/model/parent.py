from datetime import datetime, UTC
from mongoengine import Document, ObjectIdField, StringField, DateField, DateTimeField, EmailField, FileField, EmbeddedDocumentField

from Server.model.commons import LocationAddress
from Server.utils import from_appglobal


class Parent(Document):
    full_name = StringField(max_length=80, required=True)
    alternative_name = StringField(max_length=20, null=True)
    birthday = DateField(auto_now=False, auto_now_add=False)

    phone_number = StringField(max_length=15, required=True)
    email = EmailField(max_length=100, null=True)
    address = EmbeddedDocumentField(LocationAddress, required=True)

    avatar = FileField(collection_name='parents', null=True)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s %s (%s)" % (self.first_name, self.last_name, self.phone_number)

    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(Parent, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(Parent, self).update(**kwargs)
