import json

from flask import make_response

from Server.model.schoolbus import SchoolBus

from Server.utils import validate_token
from Server.utils.mongoJsonEncoder import Encoder


# School Bus Services Control
def get_school_bus(schoolbus_id: str = None):
    try:
        school_bus = SchoolBus.objects.get(id=schoolbus_id) if schoolbus_id else SchoolBus.objects()
        return make_response({"schoolbus": json.loads(school_bus.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def create_school_bus(schoolbus_data: dict):
    try:
        schoolbus_check = SchoolBus.objects(register=schoolbus_data["register"])

        if schoolbus_check:
            return make_response({'message': 'school bus already exists'}, 404)

        schoolbus = SchoolBus(
            name = schoolbus_data["name"],
            register = schoolbus_data["register"],
            seats = schoolbus_data["seats"],
            chassis = schoolbus_data["chassis"],
            model = schoolbus_data["model"],
            brand = schoolbus_data["brand"],
            status = schoolbus_data["status"]
        ).save()

        return make_response({"message": "successfully inserted", "result": str(schoolbus.id)}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def update_school_bus(schoolbus_id: str, schoolbus_data: dict):
    try:
        schoolbus = SchoolBus.objects.get(id=schoolbus_id)

        if schoolbus:
            schoolbus.name = schoolbus_data["name"]
            schoolbus.register = schoolbus_data["register"]
            schoolbus.seats = schoolbus_data["seats"]
            schoolbus.chassis = schoolbus_data["chassis"]
            schoolbus.model = schoolbus_data["model"]
            schoolbus.brand = schoolbus_data["brand"]
            schoolbus.status = schoolbus_data["status"]
            schoolbus.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "school bus does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_school_bus(schoolbus_id: str):
    try:
        schoolbus = SchoolBus.objects.get(id=schoolbus_id)
        if schoolbus:
            schoolbus.delete()

            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "school bus does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)
