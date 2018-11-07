import jwt
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from functools import wraps
from app.db.users import User


secret_key = app.config['SECRET_KEY']

def hash_password(password):
    hashed_pass = generate_password_hash(password, method='sha256')
    return hashed_pass


def verify_password(db_password, password):
    result = check_password_hash(db_password, password)
    return result


def generate_token(user_name):
    expiration_time = 30
    token = jwt.encode({'username': user_name}, secret_key, algorithm='HS256')
    return token.decode('utf-8')


def verify_token(token):
    response = jwt.decode(token, secret_key, algorithms=['HS256'])
    if response:
        user = response['username']
        return username


def is_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token_key' in request.headers:
            token = request.headers['token_key']
            try:
                data = jwt.decode(token, secret_key)
                username = data['username']
                usr = User()
                user = usr.find_user_by_username(username)
                if not user['admin']:
                    return {'message': 'sorry u not an admin, u cant access this endpoint'}
            except:
                return {'message': 'sorry, You provided an invalid token'}, 401
        if not token:
            return {'message': 'sorry, you missing a token'}, 401
        return f(*args, **kwargs)
    return decorated


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token_key' in request.headers:
            token = request.headers['token_key']
            try:
                data = jwt.decode(token, secret_key)
                username = data['username']
            except:
                return {'message': 'sorry, You provided an invalid token'}, 401
        if not token:
            return {'message': 'sorry, you missing a token'}, 401
        return f(*args, **kwargs)
    return decorated


def user_from_token():
    token = request.headers['token_key']
    try:
        data = jwt.decode(token, secret_key)
        username = data['username']
        usr = User()
        user_dict = usr.find_user_by_username(username)
        return user_dict
    except:
        return {'message': 'sorry, You provided an invalid token'}, 401


def string_validator(string_param):
    special_characters ='$#@%&*!'

    special_character = 0
    lowercase = 0
    uppercase = 0


    for character in string_param:
        if character.islower():
            lowercase +=1
        elif character.isupper():
            uppercase +=1
        elif special_characters.find(character) != -1:
            special_character +=1

    if special_character >= 1:
        return "special character exists"
    if lowercase >= 1 or uppercase >= 1:
        return "valid"

# response = string_validator('$#')
# print (response)
