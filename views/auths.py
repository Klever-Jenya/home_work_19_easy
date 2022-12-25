import calendar
import datetime
import hashlib
# import json

import jwt

from flask import request
from flask_restx import Resource, Namespace, abort


from constants import SECRET, ALGO
from models.user import User
from setup_db import db

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):

    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)

        if None in [username, password]:
            abort(400)

        user = db.session.query(User).filter(User.username == username).first()

        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

        if password_hash != user.password:
            return {"error": "Неверные учётные данные"}, 401

        data = {
            "username": user.username,
            "role": user.role
        }

        sec30 = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        data['exp'] = calendar.timegm(sec30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)

        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        # генерит пару access_token и refresh_token и отдает их в виде JSON (сейчас словарь)
        return tokens, 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            return abort(400)
        try:
            data = jwt.decode(jwt=refresh_token, key=SECRET, algorithms=[ALGO])
        except Exception as e:
            abort(400)

        username = data.get("username")
        user = db.session.query(User).filter(User.username == username).first()

        data = {
            "username": user.username,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)

        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        # генерит пару access_token и refresh_token и отдает их в виде JSON.
        return tokens, 201

