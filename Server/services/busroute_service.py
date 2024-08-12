import json

from flask import make_response
from mongoengine import Q

from Server.model.school import School
from Server.model.student import Student
from Server.model.schoolbus import SchoolBus
from Server.model.busteam import BusDriver, BusSupervisor, BusTeam
from Server.model.busroute import BusStopLocation, BusRoute, BusRouteWithLocation, BusLocationWithStudents, BusRouteHistory
from Server.model.commons import LocationAddress
from Server.model.constants import BUS_STATUS, JOURNEY_TYPE, ROUTE_STATUS

from Server.utils import validate_token
from Server.utils.mongoJsonEncoder import Encoder


# Bus Location Services Control
def get_busstop_location(busstop_id: str = None):
    try:
        busstop_location = BusStopLocation.objects.get(id=busstop_id) if busstop_id else BusStopLocation.objects()
        return make_response({"busstop" if busstop_id else "busstops": json.loads(busstop_location.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


def get_busstop_by_name(busstop_name: str):
    try:
        busstop_location = BusStopLocation.objects(name=busstop_name)
        return make_response({"busstop": json.loads(busstop_location.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def create_busstop_location(busstop_data: dict | list):
    def do_create(busstop_document: dict):
        busstop_check = BusStopLocation.objects(name=busstop_document["name"])

        if busstop_check:
            return (False, "")

        busstop_location = BusStopLocation(
            name = busstop_document["name"],
            address = LocationAddress(
                street = busstop_document["address"]["street"],
                number = busstop_document["address"]["number"],
                district = busstop_document["address"]["district"],
                province = busstop_document["address"]["province"],
                state = busstop_document["address"]["state"],
                location = busstop_document["address"]["location"]
            ),
            next_location = busstop_document["next_location"]
        ).save()
        return (True, str(busstop_location.id))
    try:
        busstop_out = []
        if isinstance(busstop_data, list):
            for busstop_document in busstop_data:
                success, busstop_id = do_create(busstop_document)
                if success:
                    busstop_out.append(busstop_id)
                else:
                    busstop_out.append(f"bus stop [ {busstop_document['name']} ] already exists")
        elif isinstance(busstop_data, dict):
            success, busstop_id = do_create(busstop_data)
            if success:
                busstop_out.append(busstop_id)
            else:
                busstop_out.append(f"bus stop [ {busstop_data['name']} ] already exists")
        
        return make_response({"message": "successfully inserted", "result": busstop_out}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def update_busstop_location(busstop_id: str, busstop_data: dict):
    try:
        busstop_location = BusStopLocation.objects.get(id=busstop_id)
        if busstop_location:
            busstop_location.address = LocationAddress(
                street = busstop_data["address"]["street"],
                number = busstop_data["address"]["number"],
                district = busstop_data["address"]["district"],
                province = busstop_data["address"]["province"],
                state = busstop_data["address"]["state"],
                location = busstop_data["address"]["location"]
            )
            busstop_location.next_location = busstop_data["next_location"]
            busstop_location.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "bus location does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_busstop_location(busstop_id: str):
    try:
        busstop_location = BusStopLocation.objects.get(id=busstop_id)
        if busstop_location:
            busstop_location.delete()

            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "bus location does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)


# Bus Routes Services Control
def get_busroute(busroute_id: str = None):
    try:
        busroute = BusRoute.objects.get(id=busroute_id) if busroute_id else BusRoute.objects()
        return make_response({"busroute": json.loads(busroute.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


def get_busroute_by_schoolbus(schoolbus_id: str = None):
    try:
        school_bus_reference = SchoolBus.objects.get(id=schoolbus_id)
        busroute = BusRoute.objects(school_bus=school_bus_reference)

        if busroute:
            return make_response({"busroute": json.loads(busroute.to_json(cls=Encoder))}, 200)
        else:
            raise f"bus route for school bus [ {schoolbus_id} ] does not exists"
    except Exception as e:
        return make_response({"message": str(e)}, 404)


def get_busroute_by_driver(busdriver_id: str = None):
    try:
        busdriver_reference = BusDriver.objects.get(id=busdriver_id)
        busroute = BusRoute.objects(bus_driver=busdriver_reference)

        if busroute:
            return make_response({"busroute": json.loads(busroute.to_json(cls=Encoder))}, 200)
        else:
            raise f"bus route for bus driver [ {busdriver_id} ] does not exists"
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def create_busroute(busroute_data: dict | list):
    def do_create(busroute_document):
        schoolbus_reference = SchoolBus.objects.get(id=busroute_document["bus_id"])
        driver_reference = BusDriver.objects.get(id=busroute_document["bus_team"]["driver_id"])
        supervisor_reference = BusSupervisor.objects.get(id=busroute_document["bus_team"]["supervisor_id"])
        school_reference = School.objects.get(id=busroute_document["school_id"])

        busroute = BusRoute(
            name = busroute_document["name"],
            school_bus = schoolbus_reference,
            bus_team = BusTeam(
                name = busroute_document["bus_team"]["name"],
                driver = driver_reference,
                supervisor = supervisor_reference
            ),
            journey_type = busroute_document["journey_type"],
            school = school_reference,
            estimated_start_time = busroute_document["estimated_start_time"],
            estimated_end_time = busroute_document["estimated_end_time"]
        ).save()
        return str(busroute.id)
    try:
        busroute_out = []
        if isinstance(busroute_data, list):
            for busroute_document in busroute_data:
                busroute_id = do_create(busroute_document)
                busroute_out.append(busroute_id)
        elif isinstance(busroute_data, dict):
            busroute_id = do_create(busroute_data)
            busroute_out.append(busroute_id)

        return make_response({"message": "successfully inserted", "result": busroute_out}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def update_busroute(busroute_id: str, busroute_data: dict):
    try:
        bus_route = BusRoute.objects.get(id=busroute_id)
        if bus_route:
            schoolbus_reference = SchoolBus.objects.get(id=busroute_data["bus_id"])
            driver_reference = BusDriver.objects.get(id=busroute_data["bus_team"]["driver_id"])
            supervisor_reference = BusSupervisor.objects.get(id=busroute_data["bus_team"]["supervisor_id"])

            bus_route.name = busroute_data["name"]
            bus_route.school_bus = schoolbus_reference
            bus_route.bus_team = BusTeam(
                name = busroute_data["bus_team"]["name"],
                driver = driver_reference,
                supervisor = supervisor_reference
            )
            bus_route.journey_type = busroute_data["journey_type"]
            bus_route.estimated_start_time = busroute_data["estimated_start_time"]
            bus_route.estimated_end_time = busroute_data["estimated_end_time"]
            bus_route.route_status = busroute_data["route_status"]
            bus_route.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "bus route does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_busroute(busroute_id: str):
    try:
        bus_route = BusRoute.objects.get(id=busroute_id)
        if bus_route:
            bus_route.delete()

            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "bus route does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)


# Bus Route With Location Services Control
def get_busroute_with_location(routelocation_id: str = None):
    try:
        route_location = BusRouteWithLocation.objects.get(id=routelocation_id) if routelocation_id else BusRouteWithLocation.objects()
        return make_response({"routelocation": json.loads(route_location.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def create_busroute_with_location(routelocation_data: dict):
    try:
        busroute_reference = BusRoute.objects.get(id=routelocation_data["busroute_id"])
        busstop_reference = BusStopLocation.objects.get(id=routelocation_data["busstop_id"])
        next_route_sequence = BusRouteWithLocation.objects.count(bus_route = busroute_reference)

        route_location = BusRouteWithLocation(
            bus_route = busroute_reference,
            busstop_location = busstop_reference,
            route_sequence = next_route_sequence + 1,
            estimated_travel_time = routelocation_data["estimated_travel_time"],
            delay_travel_time = routelocation_data["delay_travel_time"]
        ).save()

        return make_response({"message": "successfully inserted", "result": str(route_location.id)}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def update_busroute_with_location(routelocation_id: str, routelocation_data: dict):
    try:
        route_location = BusRouteWithLocation.objects.get(id=routelocation_id)
        if route_location:
            busroute_reference = BusRoute.objects.get(id=routelocation_data["busroute_id"])
            busstop_reference = BusStopLocation.objects.get(id=routelocation_data["busstop_id"])

            route_location.bus_route = busroute_reference
            route_location.busstop_location = busstop_reference
            route_location.route_sequence = routelocation_data["route_sequence"]
            route_location.estimated_travel_time = routelocation_data["estimated_travel_time"]
            route_location.delay_travel_time = routelocation_data["delay_travel_time"]
            route_location.location_status = routelocation_data["location_status"]
            route_location.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "bus route with location does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_busroute_with_location(routelocation_id: str):
    try:
        route_location = BusRouteWithLocation.objects.get(id=routelocation_id)
        if route_location:
            route_location.delete()

            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "bus route with location does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)


# Bus Location With Students Services Control
def get_busstop_location_with_students(locationtudent_id: str = None):
    try:
        location_student = BusLocationWithStudents.objects.get(id=locationtudent_id) if locationtudent_id else BusLocationWithStudents.objects()
        return make_response({"buslocationwithstudents": json.loads(location_student.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def create_busstop_location_with_students(locationstudent_data: dict):
    try:
        student_reference = Student.objects.get(id=locationstudent_data["student_id"])
        busstop_location_reference = BusStopLocation.objects.get(id=locationstudent_data["busstop_location_id"])

        location_student = BusLocationWithStudents(
            student = student_reference,
            busstop_location = busstop_location_reference
        ).save()

        return make_response({"message": "successfully inserted", "result": str(location_student.id)}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def update_busstop_location_with_students(locationstudent_id: str, locationstudent_data: dict):
    try:
        location_student = BusLocationWithStudents.objects.get(id=locationstudent_id)
        if location_student:
            busstop_location_reference = BusStopLocation.objects.get(id=locationstudent_data["busstop_location_id"])

            location_student.student_id = locationstudent_data["student_id"]
            location_student.busstop_location = busstop_location_reference
            location_student.student_status = locationstudent_data["student_status"]
            location_student.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "bus location with students does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_busstop_location_with_students(locationstudent_id: str):
    try:
        location_student = BusLocationWithStudents.objects.get(id=locationstudent_id)

        if location_student:
            location_student.delete()

            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "bus location with students does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)


# Bus Route History Services Control
def get_busroute_history(routehistory_id: str = None):
    try:
        busroute_history = BusRouteHistory.objects.get(id=routehistory_id) if routehistory_id else BusRouteHistory.objects()
        return make_response({"busroutehistory": json.loads(busroute_history.to_json(cls=Encoder))}, 200)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def create_busroute_history(routehistory_data: dict):
    try:
        route_location_reference = BusRouteWithLocation.objects.get(id=routehistory_data["routelocation_id"])
        location_student_reference = BusLocationWithStudents.objects.get(id=routehistory_data["locationstudent_id"])

        busroute_history = BusRouteHistory(
            route_location = route_location_reference,
            location_student = location_student_reference,
            route_status = routehistory_data["route_status"],
            location_status = routehistory_data["location_status"],
            student_status = routehistory_data["student_status"]
        ).save()

        return make_response({"message": "successfully inserted", "result": str(busroute_history.id)}, 201)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def update_busroute_history(routehistory_id: str, routehistory_data: dict):
    try:
        busroute_history = BusRouteHistory.objects.get(id=routehistory_id)

        if busroute_history:
            busroute_history.submit_report = routehistory_data["submit_report"]
            busroute_history.update()

            return make_response({"message": "successfully updated"}, 201)
        else:
            return make_response({"message": "bus route history does not exists"}, 404)
    except Exception as e:
        return make_response({"message": str(e)}, 404)


@validate_token
def delete_busroute_history(routehistory_id: str):
    try:
        busroute_history = BusRouteHistory.objects.get(id=routehistory_id)
        if busroute_history:
            busroute_history.delete()

            return make_response({"message" : "successfully deleted"}, 200)
        else:
            return make_response({"message" : "bus route history does not exists"}, 404)
    except Exception as e:
        return make_response({"message" : str(e)}, 404)
