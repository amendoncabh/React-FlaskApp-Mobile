import json

from mongoengine.queryset import Q
from mongoengine.errors import FieldDoesNotExist
from flask import make_response

from model.busteam import BusDriver, BusSupervisor
from model.commons import LocationAddress
from model.user import User

from Server.utils import validate_token
from Server.utils.mongoJsonEncoder import Encoder


# Bus Driver Services Control
def get_bus_driver(busdriver_id: str = None):
    try:
        busdriver = BusDriver.objects.get(id=busdriver_id) if busdriver_id else BusDriver.objects()
        return make_response({"busdriver" if busdriver_id else "busdrivers": json.loads(busdriver.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def post_bus_driver(busdriver_data: dict):
    try:
        user_reference =  User.objects(id=busdriver_data["user_id"]).get()
        if not user_reference:
            return make_response({"message": "user reference for driver does not exists"}, 404)

        driver_check = BusDriver.objects(Q(user=user_reference) | Q(full_name=busdriver_data["full_name"]))

        if driver_check:
            return make_response({"message": "driver already exists"}, 404)

        bus_driver = BusDriver(
            user = user_reference,
            full_name = busdriver_data["full_name"],
            alternative_name = busdriver_data["alternative_name"],
            birthday = busdriver_data["birthday"],
            phone_number = busdriver_data["phone_number"],
            address = LocationAddress(
                street = busdriver_data["address"]["street"],
                number = busdriver_data["address"]["number"],
                district = busdriver_data["address"]["district"],
                province = busdriver_data["address"]["province"],
                state = busdriver_data["address"]["state"],
                location = busdriver_data["address"]["location"]
            )
        ).save()

        return make_response({"message": "successfully inserted", "result": str(bus_driver.id)}, 201)
    except KeyError as e:
        return make_response({"message": f"field [ {e} ] does not sent"}, 404)
    except FieldDoesNotExist as e:
        return make_response({"message": str(e)}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


# Bus Supervisor Services Control
def get_bus_supervisor(bussupervisor_id: str = None):
    try:
        bus_supervisor = BusSupervisor.objects.get(id=bussupervisor_id) if bussupervisor_id else BusSupervisor.objects()
        return make_response({"supervisor" if bussupervisor_id else "supervisors": json.loads(bus_supervisor.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)

@validate_token
def post_bus_supervisor(bussupervisor_data: dict):
    try:
        user_reference = User.objects.get(id=bussupervisor_data["user_id"])
        if not user_reference:
            return make_response({"message": "user reference for supervisor does not exists"}, 404)

        supervisor_check = BusSupervisor.objects(Q(user=user_reference) | Q(full_name=bussupervisor_data["full_name"]))
        if supervisor_check:
            return make_response({"message": "supervisor already exists"}, 404)

        bus_supervisor = BusSupervisor(
            user = user_reference,
            full_name = bussupervisor_data["full_name"],
            alternative_name = bussupervisor_data["alternative_name"],
            birthday = bussupervisor_data["birthday"],
            phone_number = bussupervisor_data["phone_number"],
            address = LocationAddress(
                street = bussupervisor_data["address"]["street"],
                number = bussupervisor_data["address"]["number"],
                district = bussupervisor_data["address"]["district"],
                province = bussupervisor_data["address"]["province"],
                state = bussupervisor_data["address"]["state"],
                location = bussupervisor_data["address"]["location"]
            )
        ).save()

        return make_response({"message": "successfully inserted", "result": str(bus_supervisor.id)}, 201)
    except KeyError as e:
        return make_response({"message": f"field [ {e} ] does not sent"}, 404)
    except FieldDoesNotExist as e:
        return make_response({"message": str(e)}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)
