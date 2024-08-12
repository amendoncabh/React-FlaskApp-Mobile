import json

from flask import make_response
from mongoengine import Q

from Server.model.parent import Parent
from Server.model.school import School
from Server.model.student import Student
from Server.model.commons import LocationAddress

from Server.utils import validate_token
from Server.utils.mongoJsonEncoder import Encoder


# Parents Services Control
def get_parent(parent_id: str = None):
    try:
        parent = Parent.objects.get(id=parent_id) if parent_id else Parent.objects()
        return make_response({"parent" if parent_id else "parents": json.loads(parent.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def create_parent(parent_data: dict):
    try:
        parent_check = Parent.objects(Q(phone_number=parent_data["phone_number"]) | Q(email=parent_data["email"]))

        if parent_check:
            return make_response({"message": "parent already exists"}, 404)

        parent = Parent(
            full_name = parent_data["full_name"],
            alternative_name = parent_data["alternative_name"],
            birthday = parent_data["birthday"],
            phone_number = parent_data["phone_number"],
            email = parent_data["email"],
            address = LocationAddress(
                street = parent_data["address"]["street"],
                number = parent_data["address"]["number"],
                district = parent_data["address"]["district"],
                province = parent_data["address"]["province"],
                state = parent_data["address"]["state"],
                location = parent_data["address"]["location"]
            )
        ).save()

        return make_response({"message": "successfully inserted", "result": str(parent.id)}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def update_parent(parent_id: str, parent_data: dict):
    try:
        parent = Parent.objects.get(id=parent_id)
        if parent:
            parent.full_name = parent_data["full_name"]
            parent.alternative_name = parent_data["alternative_name"]
            parent.birthday = parent_data["birthday"]
            parent.phone_number = parent_data["phone_number"]
            parent.email = parent_data["email"]
            parent.address = LocationAddress(
                street = parent_data["address"]["street"],
                number = parent_data["address"]["number"],
                district = parent_data["address"]["district"],
                province = parent_data["address"]["province"],
                state = parent_data["address"]["state"],
                location = parent_data["address"]["location"]
            )
            parent.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "parent does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_parent(parent_id: str):
    try:
        parent = Parent.objects.get(id=parent_id)
        if parent:
            parent.delete()

            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "parent does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)


# Schools Services Control
def get_school(school_id: str = None):
    try:
        school = School.objects.get(id=school_id) if school_id else School.objects()
        return make_response({"school" if school_id else "schools": json.loads(school.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def create_school(school_data: dict):
    try:
        school_check = School.objects(Q(phone_number=school_data["phone_number"]) | Q(email=school_data["email"]))

        if school_check:
            return make_response({"message": "school already exists"}, 404)

        school = School(
            full_name = school_data["full_name"],
            alternative_name = school_data["alternative_name"],
            phone_number = school_data["phone_number"],
            email = school_data["email"],
            address = LocationAddress(
                street = school_data["address"]["street"],
                number = school_data["address"]["number"],
                district = school_data["address"]["district"],
                province = school_data["address"]["province"],
                state = school_data["address"]["state"],
                zip_code = school_data["address"]["zip_code"],
                location = school_data["address"]["location"]
            )
        ).save()

        return make_response({"message": "successfully inserted", "result": str(school.id)}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def update_school(school_id: str, school_data: dict):
    try:
        school = School.objects.get(id=school_id)
        if school:
            school.full_name = school_data["full_name"]
            school.alternative_name = school_data["alternative_name"]
            school.phone_number = school_data["phone_number"]
            school.email = school_data["email"]
            school.address = LocationAddress(
                street = school_data["address"]["street"],
                number = school_data["address"]["number"],
                district = school_data["address"]["district"],
                province = school_data["address"]["province"],
                state = school_data["address"]["state"],
                location = school_data["address"]["location"]
            )
            school.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "school does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_school(school_id: str):
    try:
        school = School.objects.get(id=school_id)
        if school:
            school.delete()

            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "school does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)


# Students Services Control
def get_student(student_id: str = None):
    try:
        student = Student.objects.get(id=student_id) if student_id else Student.objects()
        return make_response({"student" if student_id else "students": json.loads(student.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def create_student(student_data: dict | list):
    def do_create(student_document: dict):
        parent_reference = Parent.objects.get(id=student_document["parent_id"])
        school_reference = School.objects.get(id=student_document["school_id"])

        student_check = Student.objects(Q(first_name=student_document["first_name"]) & Q(last_name=student_document["last_name"]) & Q(parent=parent_reference))

        if student_check:
            return (False, None)

        student = Student(
            first_name = student_document["first_name"],
            last_name = student_document["last_name"],
            alternative_name = student_document["alternative_name"],
            birthday = student_document["birthday"],
            parent = parent_reference,
            school = school_reference,
            classroom = student_document["classroom"]
        ).save()
        
        return (True, str(student.id))
    try:
        students_out = []

        if isinstance(student_data, list):
            for student_document in student_data:
                success, student_id = do_create(student_document)
                if success:
                    students_out.append(student_id)
                else:
                    return make_response({"message": "student already exists"}, 404)
        elif isinstance(student_data, dict):
            success, student_id = do_create(student_data)
            if success:
                students_out.append(student_id)
            else:
                return make_response({"message": "student already exists"}, 404)

        return make_response({"message": "successfully inserted", "result": students_out}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def update_student(student_id: str, student_data: dict):
    try:
        student = Student.objects.get(id=student_id)
        if student:
            parent_reference = Parent.objects.get(id=student_data["parent_id"])
            school_reference = School.objects.get(id=student_data["school_id"])

            student.first_name = student_data["first_name"]
            student.last_name = student_data["last_name"]
            student.alternative_name = student_data["alternative_name"]
            student.birthday = student_data["birthday"]
            student.parent = parent_reference
            student.school = school_reference
            student.classroom = student_data["classroom"]
            student.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "student does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_student(student_id: str):
    try:
        student = Student.objects.get(id=student_id)
        if student:
            student.delete()

            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "student does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)
