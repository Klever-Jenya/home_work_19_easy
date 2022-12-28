from flask import request
from flask_restx import Resource, Namespace

from models.user import User, UserSchema
from setup_db import db

user_ns = Namespace('users')



@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = db.session.query(User).all()
        users = UserSchema(many=True).dump(all_users)
        return users, 200

    def post(self):
        req_json = request.json
        new_user = User(**req_json)
        with db.session.begin()
            db.session.add(new_user)
        return "", 201, {"location": f"/users/{new_user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid:int):
        try:
            user_by_id = db.session.query(User).get(uid)
            user = UserSchema().dump(user_by_id)
            return user, 200
        except Exception as e:
            return str(e), 404

    def put(self, uid):
        user = db.session.query(User).get(uid)
        req_json = request.json
        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.role = req_json.get("role")
        db.session.add(user)
        db.session.commit()
        return "", 204