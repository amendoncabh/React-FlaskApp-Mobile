from flask import Blueprint, request

from Server.services.busteam_service import (
    get_bus_driver,
    post_bus_driver,
    get_bus_supervisor,
    post_bus_supervisor
)


busdrivers_bp = Blueprint(name='busdrivers', import_name=__name__, url_prefix="/api/v2/busdrivers")
bussupervisor_bp = Blueprint(name='bussupervisors', import_name=__name__, url_prefix="/api/v2/bussupervisors")


# Bus Drivers Routes
@busdrivers_bp.route("/all", methods=['GET'])
def get_busdriver_all():
    return get_bus_driver()


@busdrivers_bp.route("/<busdriver_id>", methods=['GET'])
def get_busdriver_id(busdriver_id: str):
    return get_bus_driver(busdriver_id)


@busdrivers_bp.route("/add", methods=['POST'])
def post_busdriver():
    busdriver_data = request.get_json()
    return post_bus_driver(busdriver_data)


# Bus Supervisor Routes
@bussupervisor_bp.route("/all", methods=['GET'])
def get_bussupervisor_all():
    return get_bus_supervisor()


@bussupervisor_bp.route("/<supervisor_id>", methods=['GET'])
def get_bussupervisor_id(supervisor_id: str):
    return get_bus_supervisor(supervisor_id)


@bussupervisor_bp.route("/add", methods=['POST'])
def post_bussupervisor():
    supervisor_data = request.get_json()
    return post_bus_supervisor(supervisor_data)
