import os
from app import api
from flask_restplus import Resource, fields
from app.db.users import User
from app.utils.helpers import generate_token, provide_token, is_admin

user_model = api.model('User', {
    'username': fields.String(description='username', required=True, min_length=2),
    'password': fields.String(description='password', required=True)
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