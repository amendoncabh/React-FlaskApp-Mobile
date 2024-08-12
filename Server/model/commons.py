from mongoengine import EmbeddedDocument, StringField, PointField


class LocationAddress(EmbeddedDocument):
    """Data address for locations (home address, bus routes, tec.).
    """
    street = StringField(max_length=150, null=True)
    number = StringField(max_length=10, null=True)
    district = StringField(max_length=50, null=True)
    province = StringField(max_length=30, null=True)
    state = StringField(max_length=2, null=True)
    zip_code = StringField(max_length=10, null=True, default=None)
    location = PointField(null=True)    # latitude, longitude
