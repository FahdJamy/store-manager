import jwt
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from functools import wraps
from app.db.users import User


secret_key = app.config['SECRET_KEY']

def generate_token(user_name):
    expiration_time = 30
    token = jwt.encode({'username': user_name}, secret_key, algorithm='HS256')
    return token.decode('utf-8')


def verify_token(token):
    response = jwt.decode(token, secret_key, algorithms=['HS256'])
    if response:
        user = response['username']
        return username


def provide_token(f):
    @wraps(f)
    def wraping_func(*args, **kwargs):
        token = None

        if 'token_key' in request.headers:
            token = request.headers['token_key']
            try:
                data = jwt.decode(token, secret_key)
                return data['username']
            except:
                return {'message' : 'sorry, You provided an invalid token'}, 401
        if not token:
            return {'message': 'sorry, you missing a token'}, 401
        return f(*args, **kwargs)
    return wraping_func


def is_admin(f):
    @wraps (f)
    def decorated(*args, **kwargs):
        token =  None
        
        if 'token_key' in  request.headers:
            token = request.headers['token_key']
            try :
                data = jwt.decode(token, secret_key)
                username = data['username']
                usr = User()
                user = usr.find_user_by_username(username)
                if not user['admin']:
                    return {'message' : 'sorry u not an admin, u cant access this endpoint'}
            except :
                return {'message' : 'sorry, You provided an invalid token'}, 401
        if not token:
            return {'message' : 'sorry, you missing a token'}, 401
        return f(*args, **kwargs)
    return decorated
