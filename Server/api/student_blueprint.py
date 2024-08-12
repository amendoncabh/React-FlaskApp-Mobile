from flask import Blueprint, request

from Server.services.student_service import (
    get_parent,
    create_parent,
    update_parent,
    delete_parent,
    get_school,
    create_school,
    update_school,
    delete_school,
    get_student,
    create_student,
    update_student,
    delete_student
)

parents_bp = Blueprint(name='parents', import_name=__name__, url_prefix="/api/v2/parents")
schools_bp = Blueprint(name='schools', import_name=__name__, url_prefix="/api/v2/schools")
students_bp = Blueprint(name='students', import_name=__name__, url_prefix="/api/v2/students")


# Parents Routes
@parents_bp.route("/all", methods=['GET'])
def get_parent_all():
    return get_parent()


@parents_bp.route("/<parent_id>", methods=['GET'])
def get_parent_id(parent_id: str):
    return get_parent(parent_id)


@parents_bp.route("/add", methods=['POST'])
def post_parent():
    parent_data = request.get_json()
    return create_parent(parent_data)


@parents_bp.route("/update/<parent_id>", methods=['PUT'])
def put_parent(parent_id: str):
    parent_data = request.get_json()
    return update_parent(parent_id, parent_data)


@parents_bp.route("/delete/<parent_id>", methods=['DELETE'])
def deleter_parent(parent_id: str):
    return delete_parent(parent_id)


# Schools Routes
@schools_bp.route("/all", methods=['GET'])
def get_school_all():
    return get_school()


@schools_bp.route("/<school_id>", methods=['GET'])
def get_school_id(school_id: str):
    return get_school(school_id)


@schools_bp.route("/add", methods=['POST'])
def post_school():
    school_data = request.get_json()
    return create_school(school_data)


@schools_bp.route("/update/<school_id>", methods=['PUT'])
def put_school(school_id: str):
    school_data = request.get_json()
    return update_school(school_id, school_data)


@schools_bp.route("/delete/<school_id>", methods=['DELETE'])
def deleter_school(school_id: str):
    return delete_school(school_id)


# Students Routes
@students_bp.route("/all", methods=['GET'])
def get_student_all():
    return get_student()


@students_bp.route("/<student_id>", methods=['GET'])
def get_student_id(student_id: str):
    return get_student(student_id)


@students_bp.route("/add", methods=['POST'])
def post_student():
    student_data = request.get_json()
    return create_student(student_data)


@students_bp.route("/update/<student_id>", methods=['PUT'])
def put_student(student_id: str):
    student_data = request.get_json()
    return update_student(student_id, student_data)


@students_bp.route("/delete/<student_id>", methods=['DELETE'])
def deleter_student(student_id: str):
    return delete_student(student_id)
