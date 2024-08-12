from flask import Blueprint, request

from Server.services.busroute_service import (
    get_busstop_location,
    get_busstop_by_name,
    create_busstop_location,
    update_busstop_location,
    delete_busstop_location,
    get_busroute,
    get_busroute_by_schoolbus,
    get_busroute_by_driver,
    create_busroute,
    update_busroute,
    delete_busroute,
    get_busroute_with_location,
    create_busroute_with_location,
    update_busroute_with_location,
    delete_busroute_with_location,
    get_busstop_location_with_students,
    create_busstop_location_with_students,
    update_busstop_location_with_students,
    delete_busstop_location_with_students,
    get_busroute_history,
    create_busroute_history,
    update_busroute_history,
    delete_busroute_history
)

stoplocations_bp = Blueprint(name='stoplocations', import_name=__name__, url_prefix="/api/v2/stoplocations")
busroutes_bp = Blueprint(name='busroutes', import_name=__name__, url_prefix="/api/v2/busroutes")
routelocations_bp = Blueprint(name='routelocations', import_name=__name__, url_prefix="/api/v2/routelocations")
locationstudents_bp = Blueprint(name='locationstudents', import_name=__name__, url_prefix="/api/v2/locationstudents")
routehistories_bp = Blueprint(name='routehistories', import_name=__name__, url_prefix="/api/v2/routehistories")


# Bus Location Routes
@stoplocations_bp.route("/all", methods=['GET'])
def get_busstop_all():
    return get_busstop_location()


@stoplocations_bp.route("/<busstop_id>", methods=['GET'])
def get_busstop_id(busstop_id: str):
    return get_busstop_location(busstop_id)


@stoplocations_bp.route("/name/<busstop_name>", methods=['GET'])
def get_busstop_name(busstop_name: str):
    return get_busstop_by_name(busstop_name)


@stoplocations_bp.route("/add", methods=['POST'])
def post_busstop_location():
    busstop_data = request.get_json()
    return create_busstop_location(busstop_data)


@stoplocations_bp.route("/update/<busstop_id>", methods=['PUT'])
def put_busstop_location(busstop_id: str):
    busstop_data = request.get_json()
    return update_busstop_location(busstop_id, busstop_data)


@stoplocations_bp.route("/delete/<busstop_id>", methods=['DELETE'])
def deleter_busstop_location(busstop_id: str):
    return delete_busstop_location(busstop_id)


# Bus Route Routes
@busroutes_bp.route("/all", methods=['GET'])
def get_busroute_all():
    return get_busroute()


@busroutes_bp.route("/<busroute_id>", methods=['GET'])
def get_busroute_id(busroute_id: str):
    return get_busroute(busroute_id)


@busroutes_bp.route("/schoolbus/<schoolbus_id>", methods=['GET'])
def get_busroute_schoolbus_id(schoolbus_id: str):
    return get_busroute_by_schoolbus(schoolbus_id)


@busroutes_bp.route("/busdriver/<busdriver_id>", methods=['GET'])
def get_busroute_busdriver_id(busdriver_id: str):
    return get_busroute_by_driver(busdriver_id)


@busroutes_bp.route("/add", methods=['POST'])
def post_busroute_add():
    busroute_data = request.get_json()
    return create_busroute(busroute_data)


@busroutes_bp.route("/update/<busroute_id>", methods=['PUT'])
def put_busroute(busroute_id: str):
    busroute_data = request.get_json()
    return update_busroute(busroute_id, busroute_data)


@busroutes_bp.route("/delete/<busroute_id>", methods=['DELETE'])
def deleter_busroute(busroute_id: str):
    return delete_busroute(busroute_id)


# Bus Route With Location Routes
@routelocations_bp.route("/all", methods=['GET'])
def get_busroutewithlocation_all():
    return get_busroute_with_location()


@routelocations_bp.route("/<routelocation_id>", methods=['GET'])
def get_busroutewithlocation_id(routelocation_id: str):
    return get_busroute_with_location(routelocation_id)


@routelocations_bp.route("/add", methods=['POST'])
def post_busroutewithlocation():
    routelocation_data = request.get_json()
    return create_busroute_with_location(routelocation_data)


@routelocations_bp.route("/update/<routelocation_id>", methods=['PUT'])
def put_busroutewithlocation(routelocation_id: str):
    routelocation_data = request.get_json()
    return update_busroute_with_location(routelocation_id, routelocation_data)


@routelocations_bp.route("/delete/<routelocation_id>", methods=['DELETE'])
def delete_busroutewithlocation(routelocation_id: str):
    return delete_busroute_with_location(routelocation_id)


# Bus Location With Students Routes
@locationstudents_bp.route("/all", methods=['GET'])
def get_locationstudents_all():
    return get_busstop_location_with_students()


@locationstudents_bp.route("/<locationstudent_id>", methods=['GET'])
def get_busstop_location_with_students_id(locationstudent_id: str):
    return get_busstop_location_with_students(locationstudent_id)


@locationstudents_bp.route("/add", methods=['POST'])
def post_locationstudents():
    locationstudent_data = request.get_json()
    return create_busstop_location_with_students(locationstudent_data)


@locationstudents_bp.route("/update/<locationstudent_id>", methods=['PUT'])
def put_locationstudents(locationstudent_id: str):
    locationstudent_data = request.get_json()
    return update_busstop_location_with_students(locationstudent_id, locationstudent_data)


@locationstudents_bp.route("/delete/<locationstudents_id>", methods=['DELETE'])
def delete_locationstudents(locationstudent_id: str):
    return delete_busstop_location_with_students(locationstudent_id)


# Bus Route History Routes
@routehistories_bp.route("/all", methods=['GET'])
def get_routehistory_all():
    return get_busroute_history()


@routehistories_bp.route("/<routehistory_id>", methods=['GET'])
def get_routehistory_id(routehistory_id: str):
    return get_busroute_history(routehistory_id)


@routehistories_bp.route("/add", methods=['POST'])
def post_busroutehistory():
    routehistory_data = request.get_json()
    return create_busroute_history(routehistory_data)


@routehistories_bp.route("/update/<routehistory_id>", methods=['PUT'])
def put_busroutehistory(routehistory_id: str):
    routehistory_data = request.get_json()
    return update_busroute_history(routehistory_id, routehistory_data)


@routehistories_bp.route("/delete/<routehistory_id>", methods=['DELETE'])
def delete_busroutehistory(routehistory_id: str):
    return delete_busroute_history(routehistory_id)
