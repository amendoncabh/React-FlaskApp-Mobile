from datetime import datetime, timedelta, UTC
from jwt.utils import get_int_from_datetime
from flask import make_response
from mongoengine import Q

from Server.utils import encrypt_password, compare_passwords, generate_token
from Server.model.user import User


def post_sign_up(user_data: dict):
    try:
        user_check = User.objects(Q(email=user_data['email']) | Q(phone_number=user_data['phone_number']))

        if user_check:
            return {"status": 404, "message": "user already exists"}

        user = User(
            email = user_data['email'], 
            phone_number = user_data['phone_number'],
            first_name = user_data['first_name'],
            last_name = user_data['last_name'],
            password = encrypt_password(user_data['password'])
        ).save()

        return make_response({'message': 'successfully inserted', "result": str(user.id)}, 201)

    except KeyError as e:
        return make_response({"message": f"field [ {e} ] does not sent"}, 404)
    except Exception as e:
        return make_response({'message': str(e)}, 404)


def post_sign_in(credentials: dict):
    try:
        user = User.objects.get(Q(email=credentials['username']) | Q(phone_number=credentials['username']))

        if user and compare_passwords(credentials["password"], user.password):
            payload = {
                "sub": str(user.id),
                "iat": get_int_from_datetime(datetime.now(UTC)),
                "exp": get_int_from_datetime(datetime.now(UTC) + timedelta(minutes=720))
            }
            auth_token = generate_token(payload)
            return make_response({"token": auth_token}, 200)

        return make_response({"message": "username or password invalid"}, 403)
    except Exception as e:
        return make_response({"message": str(e)}, 404)
