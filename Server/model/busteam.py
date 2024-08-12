from datetime import datetime, UTC
from mongoengine import Document, EmbeddedDocument, ObjectIdField, StringField, DateField, DateTimeField, EmailField, ImageField, FileField, BooleanField, ReferenceField, EmbeddedDocumentField

from model.commons import LocationAddress
from model.user import User

from utils import from_appglobal


class BusDriver(Document):
    user = ReferenceField(User, dbref=True, required=True)

    full_name = StringField(max_length=80)
    alternative_name = StringField(max_length=20, null=True)
    birthday = DateField(required=True)

    phone_number = StringField(max_length=15, null=True)
    email = EmailField(null=True)
    image = ImageField(collection_name='drivers', null=True)

    address = EmbeddedDocumentField(LocationAddress, required=True)

    enabled = BooleanField(default=True)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s (%s)" % (self.alternative_name | self.full_name, self.phone_number)
    
    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(BusDriver, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(BusDriver, self).update(**kwargs)


class BusSupervisor(Document):
    user = ReferenceField(User, dbref=True, required=True)

    full_name = StringField(max_length=80)
    alternative_name = StringField(max_length=20, null=True)
    birthday = DateField(auto_now=False, auto_now_add=False)

    phone_number = StringField(max_length=50)
    avatar = FileField(collection_name='supervisors', max_length=100)

    address = EmbeddedDocumentField(LocationAddress, required=True)

    enabled = BooleanField(default=True)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s (%s)" % (self.alternative_name | self.full_name, self.phone_number)
    
    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(BusSupervisor, self).save(*args, **kwargs)
    
    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(BusSupervisor, self).update(**kwargs)


class BusTeam(EmbeddedDocument):
    name = StringField(max_length=20)
    driver = ReferenceField(BusDriver, dbref=True, required=True)
    supervisor = ReferenceField(BusSupervisor, dbref=True, required=True)
