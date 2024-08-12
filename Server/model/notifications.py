from datetime import datetime, UTC
from mongoengine import Document, StringField, IntField, DateField, DateTimeField, BooleanField, ReferenceField
from mongoengine.queryset import CASCADE

from student import Student
from schoolBus import BusLocationWithStudents

class NotificationTemplate(Document):
    notification_type = IntField()
    text = StringField(max_length=200)

    def __str__(self):
        return self.notification_type


class NotificationLog(Document):
    route_type = StringField(max_length=100)
    route_name = StringField(max_length=500)
    logging_time = DateTimeField(required=True, default=datetime.now(UTC))
    sender = StringField(max_length=200)
    receiver = StringField(max_length=50, null=True)
    student = ReferenceField(Student, dbref=True)
    content = StringField(max_length=500)

    def __str__(self):
        return "%s to %s: %s" % (self.sender, self.receiver, self.content)


class Attendance(Document):
    bus_location_with_student_id = ReferenceField(BusLocationWithStudents, reverse_delete_rule=CASCADE)
    status = IntField()
    current_date = DateField()
    reason_for_absence_or_missing = StringField(null=True)
    report_absence_by_parent = BooleanField(default=False)

    def __str__(self):
        return "%s => %s - status: %s / absence_by_parent: %s" % (
            self.current_date, self.bus_location_with_student_id, self.status,
            self.report_absence_by_parent)
