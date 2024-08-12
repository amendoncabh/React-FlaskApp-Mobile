from datetime import datetime, UTC
from mongoengine import Document, ObjectIdField, StringField, IntField, PolygonField, DateField, DateTimeField, BooleanField, ReferenceField, EmbeddedDocumentField
from mongoengine.queryset import CASCADE

from Server.model.school import School
from Server.model.student import Student
from Server.model.schoolbus import SchoolBus
from Server.model.busteam import BusTeam
from Server.model.commons import LocationAddress
from Server.model.constants import JOURNEY_TYPE, ROUTE_STATUS, LOCATION_STATUS, STUDENT_STATUS

from Server.utils import from_appglobal


class BusStopLocation(Document):
    name = StringField(max_length=200, required=True)
    address = EmbeddedDocumentField(LocationAddress, required=True)
    next_location = PolygonField(null=True, default=None)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s, %s - %s/%s" % (self.address.street, self.address.number, self.address.district, self.address.province)

    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(BusStopLocation, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(BusStopLocation, self).update(**kwargs)


class BusRoute(Document):
    name = StringField(max_length=20, required=True)

    school_bus = ReferenceField(SchoolBus, reverse_delete_rule=CASCADE, required=True)
    bus_team = EmbeddedDocumentField(BusTeam, required=True)
    journey_type = StringField(min_length=2, max_length=2, choices=JOURNEY_TYPE.options, default=JOURNEY_TYPE.default, required=True, unique_with=("school_bus","bus_team"))

    school = ReferenceField(School, dbref=True, reverse_delete_rule=CASCADE, required=True)

    estimated_start_time = StringField(min_length=5, max_length=5, required=True)
    estimated_end_time = StringField(min_length=5, max_length=5, required=True)

    route_status = IntField(min_value=0, max_value=2, choices=ROUTE_STATUS, default=0)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s, %s: %s" % (self.name, JOURNEY_TYPE.options[self.journey_type][1], ROUTE_STATUS[self.route_status][1])

    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(BusRoute, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(BusRoute, self).update(**kwargs)


class BusRouteWithLocation(Document):
    bus_route = ReferenceField(BusRoute, dbref=True, reverse_delete_rule=CASCADE)
    busstop_location = ReferenceField(BusStopLocation, dbref=True, reverse_delete_rule=CASCADE)
    route_sequence = IntField(required=True, default=0, unique_with="bus_route")

    # travel times in minutes from previous point
    estimated_travel_time = IntField(required=True, min_value=1, max_value=60)
    delay_travel_time = IntField(required=True, min_value=0, max_value=60)

    location_status = IntField(min_value=0, max_value=1, choices=LOCATION_STATUS, default=0)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s: %s, %s" % (self.route_sequence, self.busstop_location.name, self.bus_route.name)

    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(BusRouteWithLocation, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(BusRouteWithLocation, self).update(**kwargs)


class BusLocationWithStudents(Document):
    student = ReferenceField(Student, dbref=True, reverse_delete_rule=CASCADE, required=True)
    bus_location = ReferenceField(BusStopLocation, dbref=True, reverse_delete_rule=CASCADE, unique_with="student")

    student_status = IntField(min_value=0, max_value=6, choices=STUDENT_STATUS, default=0)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s: %s | %s" % (self.bus_location, self.student, STUDENT_STATUS[self.student_status][1])

    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(BusLocationWithStudents, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(BusLocationWithStudents, self).update(**kwargs)


class BusRouteHistory(Document):
    history_date = DateTimeField(required=True, default=datetime.now(UTC))
    route_location = ReferenceField(BusRouteWithLocation, dbref=True, reverse_delete_rule=CASCADE)
    location_student = ReferenceField(BusLocationWithStudents, dbref=True, reverse_delete_rule=CASCADE)
    
    route_status = IntField(min_value=0, max_value=2, choices=ROUTE_STATUS, default=0)
    location_status = IntField(min_value=0, max_value=1, choices=LOCATION_STATUS, default=0)
    student_status = IntField(min_value=0, max_value=6, choices=STUDENT_STATUS, default=0)
    
    submit_report = BooleanField(required=True, default=True)

    created_on = DateTimeField(null=True, default=None)
    created_by = ObjectIdField(null=True, default=None)

    updated_on = DateTimeField(null=True, default=None)
    updated_by = ObjectIdField(null=True, default=None)

    def __str__(self):
        return "%s: %s,%s" % (self.history_date, self.route_location, self.student_status)

    def save(self, *args, **kwargs):
        self.created_on = datetime.now(UTC)
        self.created_by = from_appglobal("user_id")
        return super(BusRouteHistory, self).save(*args, **kwargs)

    def update(self, **kwargs):
        self.updated_on = datetime.now(UTC)
        self.updated_by = from_appglobal("user_id")
        return super(BusRouteHistory, self).update(**kwargs)
