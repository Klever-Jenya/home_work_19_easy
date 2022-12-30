import hashlib

from flask import Flask
from flask_restx import Api

from config import Config
from models.user import User
from setup_db import db
from views.auths import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):  # регистрация, вызовы функций
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.create_all()

        password = "my_little_pony"
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        u1 = User(username="vasya", password=password_hash, role="user")

        password = "my_little_pony"
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        u2 = User(username="petya", password=password_hash, role="user")

        password = "my_little_pony"
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        u3 = User(username="oleg", password=password_hash, role="admin")

        with db.session.begin():
            db.create_all()
            db.session.add_all([u1, u2, u3])


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
