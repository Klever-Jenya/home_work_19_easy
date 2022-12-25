from flask import request
from flask_restx import Resource, Namespace

from functions.requireds import auth_required, admin_required
from models.director import Director, DirectorSchema
from setup_db import db

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        request_json = request.json
        new_director = Director(**request_json)

        db.session.add(new_director)
        db.session.commit()

        return "Director created", 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, uid):
        director = Director.query.get(uid)
        request_json = request.json
        if "name" in request_json:
            director.name = request_json.get("name")

        db.session.add(director)
        db.session.commit()

        return "", 204

    @admin_required
    def delete(self, uid: int):
        director = db.session.query(Director).get(uid)
        if not director:
            return "", 404

        db.session.delete(director)
        db.session.commit()

        return "", 204