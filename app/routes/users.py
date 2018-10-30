import os
from app import api
from flask_restplus import Resource, fields
from app.db.users import User
from app.utils.helpers import generate_token, provide_token, is_admin

user_model = api.model('User', {
    'username': fields.String(description='username', required=True, min_length=2),
    'password': fields.String(description='password', required=True)
})
update_model = api.model('User Promote To Admin Model', {
    'admin': fields.Boolean(description='Promote sales attendant to be admin by setting a true value to this field', default=False)
})
Authorization = {'token_key': {
    'in': 'header',
    'type': 'JWT',
            'description': 'Token is required'
}}
users_model = User()

""" Create a new user attendant """


@api.route('/auth/signup')
class Users (Resource):

    @api.doc(params=Authorization, required=True)
    @is_admin
    @api.expect(user_model, validate=True)
    def post(self):
        user_data = api.payload
        username = user_data['username'].strip().capitalize()
        passcode = user_data['password'].strip()
        new_user = users_model.create_user(username, passcode)
        if new_user == 'success':
            return {'message': 'User succefully registered'}, 201
        return {'message': 'sorry username is already taken'}, 400


""" User Login route (Both sales attendants and store owner) """


@api.route('/auth/login')
class Users (Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        user_data = api.payload
        username = user_data['username'].strip().capitalize()
        passcode = user_data['password'].strip()
        user = users_model.verify_username_and_password(username, passcode)
        if user == 'no user':
            return {'message': 'Sorry user {} doesnot exist, login with valid credentials'.format(username)}, 400
        if user == 'success':
            token = generate_token(username)
            return {'token': token}, 200
        return {'message': 'sorry username and password dont match, please login with valid credentials'}, 400


""" API endpoint to promote a sales attendant to an admin"""


@api.route('/user/<int:user_id>')
class Users (Resource):

    @api.doc(params=Authorization, required=True)
    @is_admin
    @api.expect(update_model, validate=True)
    def put(self, user_id):
        update_info = api.payload
        admin = update_info['admin']
        update_response = users_model.update_user_info(user_id, admin)
        if update_response != 'user with id {} is not found'.format(user_id):
            return {'message': 'user has been promoted to an admin'}
        return {'message': update_response}