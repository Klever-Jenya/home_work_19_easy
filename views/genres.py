from flask import request
from flask_restx import Resource, Namespace

from functions.requireds import auth_required, admin_required
from models.genre import Genre, GenreSchema
from setup_db import db

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = db.session.query(Genre).all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        request_json = request.json
        new_genre = Genre(**request_json)

        with db.session.begin():
            db.session.add(new_genre)

        return "genre created", 201


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = db.session.query(Genre).get(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, uid):
        updated_rows = db.session.query(Genre).filter(Genre.id == uid).update(request.json)  # int

        if updated_rows != 1:
            return "", 400

        db.session.commit()
        return "", 204

    @admin_required
    def delete(self, uid):
        genre = db.session.query(Genre).get(uid)
        if not genre:
            return "", 404

        db.session.delete(genre)
        db.session.commit()

        return "", 204