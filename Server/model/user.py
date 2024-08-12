from datetime import datetime, UTC
from mongoengine import EmbeddedDocument, Document, StringField, EmailField, DateTimeField, BooleanField, EmbeddedDocumentListField, ListField, ReferenceField


class Rule(EmbeddedDocument):
    name = StringField(max_length=20, required=True)
    endpoint = StringField(max_length=50, required=True)
    can_run = BooleanField(default=False)

    def __str__(self):
        return "%s: %s" % (self.name, self.endpoint)


class Role(Document):
    name = StringField(max_length=20, required=True)
    description = StringField(max_length=30, required=True)
    administrative = BooleanField(default=False)

    accesses = EmbeddedDocumentListField(Rule, required=True)

    def __str__(self):
        return self.name


class User(Document):
    email = EmailField(required=True)
    phone_number = StringField(max_length=15, required=True)
    password = StringField(required=True, max_length=1024)

    first_name = StringField(max_length=20, required=True)
    last_name = StringField(max_length=20, required=True)

    administrator = BooleanField(default=False)
    roles = ListField(ReferenceField(Role, dbref=True), null=True, default=None)

    reset_pass = BooleanField(default=False)
    enabled = BooleanField(default=True)

    created_on = DateTimeField(required=True, default=datetime.now(UTC))
    updated_on = DateTimeField(null=True, default=None)
    last_login = DateTimeField(null=True, default=None)

    def __str__(self):
        return "%s %s (%s)" % (self.first_name, self.last_name, self.phone_number)

    def add_role(self, role_name: str):
        roles = Role.objects.get(name=role_name)

        if roles:
            if self.roles is None:
                self.roles = ListField(ReferenceField(Role, dbref=True), null=True, default=None)
            for role in roles:
                self.roles.append(role.id)
