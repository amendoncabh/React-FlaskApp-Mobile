from flask import Blueprint, request
from services.user_service import post_sign_up, post_sign_in


users_bp = Blueprint(name = "users", import_name = __name__, url_prefix = "/api/v2/users")


@users_bp.route("/signup", methods=['POST'])
def post_signup():
    user_data = request.get_json()
    return post_sign_up(user_data)


@users_bp.route("/signin", methods=['POST'])
def post_signin():
    credentials = request.get_json()
    return post_sign_in(credentials)
