from datetime import datetime, UTC
from mongoengine import Document, ObjectIdField, StringField, DateField, DateTimeField, ImageField, ReferenceField, BooleanField
from mongoengine.queryset import CASCADE

from Server.model.parent import Parent
from Server.model.school import School

from Server.utils import from_appglobal


class Student(Document):
    first_name = StringField(max_length=20, required=True)
    last_name = StringField(max_length=20, required=True)
    alternative_name = StringField(max_length=40, null=True)
    birthday = DateField(required=True)

    parent = ReferenceField(Parent, dbref=True, reverse_delete_rule=CASCADE, required=True)
    school = ReferenceField(School, dbref=True, reverse_delete_rule=CASCADE, required=True)
    classroom = StringField(max_length=20, null=True)

    enabled = BooleanField(default=True)

    image = ImageField(collection_name='students', null=True)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s %s (%s)" % (self.first_name, self.last_name, self.phone_number)

    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(Student, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(Student, self).update(**kwargs)
