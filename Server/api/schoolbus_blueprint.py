from flask import Blueprint, request

from services.schoolbus_service import (
    get_school_bus,
    create_school_bus,
    update_school_bus,
    delete_school_bus
)

schoolbus_bp = Blueprint(name='schoolbus', import_name=__name__, url_prefix="/api/v2/schoolbus")


# School Bus Routes
@schoolbus_bp.route("/all", methods=['GET'])
def get_schoolbus_all():
    return get_school_bus()


@schoolbus_bp.route("/<busdriver_id>", methods=['GET'])
def get_schoolbus_id(busdriver_id: str):
    return get_school_bus(busdriver_id)


@schoolbus_bp.route("/add", methods=['POST'])
def post_schoolbus():
    schoolbus_data = request.get_json()
    return create_school_bus(schoolbus_data)


@schoolbus_bp.route("/update/<busdriver_id>", methods=['PUT'])
def put_schoolbus(busdriver_id: str):
    schoolbus_data = request.get_json()
    return update_school_bus(busdriver_id, schoolbus_data)


@schoolbus_bp.route("/delete/<busdriver_id>", methods=['DELETE'])
def delete_schoolbus(busdriver_id: str):
    return delete_school_bus(busdriver_id)
