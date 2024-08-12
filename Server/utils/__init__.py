import bcrypt

from typing import Any

from jwt import JWT, supported_key_types
from flask import make_response, request, current_app, g
from werkzeug.local import LocalProxy

jwt_instance = JWT()

# app info
def from_appglobal(key: str, default: Any = None):
    """
    Configuration method to return key content
    """
    if g and key in g:
        result = g.get(key, default)
        if result and not isinstance(result, str):
            result = LocalProxy(result)
    return result

# app security
def encrypt_password(password: str):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def compare_passwords(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf-8'))


def generate_token(payload):
    secret_key = supported_key_types()["oct"](current_app.config["SECRET_KEY"].encode())
    return jwt_instance.encode(payload, secret_key, "HS256")


def validate_token(f):
    def wrapper(*args, **kwargs):
        try:
            authorization = request.headers['Authorization']
            session_token = authorization.split(" ")[1]

            secret_key = supported_key_types()["oct"](current_app.config["SECRET_KEY"].encode())
            payload = jwt_instance.decode(session_token, secret_key, algorithms=["HS256"])
            
            g.user_id = payload["sub"]

            return f(*args, **kwargs)
        except Exception as e:
            return make_response({"message": str(e)}, 403)
    return wrapper
