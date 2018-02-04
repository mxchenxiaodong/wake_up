import time
import datetime

import jwt

from app import app, db

class User(db.Document):
    phone = db.StringField(required=True, unique=True)
    name = db.StringField(max_length=200, default='')
    email = db.StringField(max_length=200, default='')
    password = db.StringField(required=True, max_length=200)
    created_at = db.IntField(required=True, default=int(time.time()))
    is_admin = db.BooleanField(default=False)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            # 如果已经在blacklist里了，则直接重新登录
            if BlacklistToken.check_blacklist(auth_token):
                return 'Token blacklisted. Please log in again.'

            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Document):
    token = db.StringField(required=True, unique=True)
    created_at = db.IntField(required=True, default=int(time.time()))

    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.objects(token=auth_token).first()
        if res:
            return True
        else:
            return False

class TimeRecord(db.Document):
    created_at = db.IntField(required=True, default=int(time.time()))