import hashlib
# from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from marshmallow import Schema, fields

from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()


# Затем у тебя не получается проверить auth/ потому что
# ты при создании записей в бд для пользователя (тестовые 3 пользователя)
# не делаешь hash до добавления в базу и поэтому
# вот это строчка сравнения просто строку и хэш (файл auths.py строка 37):
#
# if password_hash != user.password:
# Исправь пожалуйста)
def get_hash(self):
    return hashlib.md5(self.password.encode('utf-8')).hexdigest()

# def get_hash(password):
#     return hashlib.pbkdf2_hmac(
#         'sha256',
#         password.encode('utf-8'),  # Convert the password to bytes
#         PWD_HASH_SALT,
#         PWD_HASH_ITERATIONS
#     ).decode("utf-8", "ignore")
