from datetime import datetime, UTC
from flask import g as app_context
from mongoengine import Document, ObjectIdField, StringField, DecimalField, DateTimeField, IntField, BooleanField, ReferenceField

from utils import from_appglobal


class ProductCategory(Document):
    name = StringField(required=True, max_length=20)

    def __str__(self):
        return self.name


class Product(Document):
    title = StringField(required=True, max_length=200)
    description = StringField(required=True, max_length=500)
    category = ObjectIdField(null=True, default=None)

    enabled = BooleanField(default=True)
    price = DecimalField(required=True, precision=2)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s (%s)" % (self.title, self.price)

    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(Product, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(Product, self).update(**kwargs)


class Order(Document):
    product = ReferenceField(Product, dbref=True)
    quantity = IntField(required=True, min_value=1)
    amount = DecimalField(required=True, precision=2)

    def __str__(self):
        return self.pk
