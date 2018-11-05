from app import api
from flask_restplus import Resource, fields
from app.db.categories import Category
from app.utils.helpers import is_admin, string_validator

category_info = api.model('Category', {
    'name': fields.String(description='category name', required=True, min_length=2),
    'description': fields.String(description='category description', required=True, min_length=2)
})
update_info = api.model('Category update model', {
    'name': fields.String(description='category name', min_length=2),
    'description': fields.String(description='category description', min_length=2)
})
Authorization = {'token_key': {
    'in': 'header',
    'type': 'JWT',
            'description': 'Token is required'
}}
category_model = Category()


""" Class for creating a new category, updating its information and deleting it """


@api.route('/categories')
class CreateCategory (Resource):

    @api.doc(params=Authorization, required=True)
    @is_admin
    @api.expect(category_info, validate=True)
    def post(self):
        category_data = api.payload
        category_name = category_data['name'].strip().capitalize()
        description = category_data['description']
        validate_category_name = string_validator(category_name)
        if validate_category_name == 'special character exists':
            return {'message' : 'sorry category name shouldnt have a special character including ($#@%)'}, 400
        if not validate_category_name:
            return {'message' : 'sorry category name shouldnt be of spaces only'}, 400
        new_category = category_model.create_category(
            category_name, description)
        if new_category == 'category created successfully':
            return {'message': 'category has been successfully created !!!'}, 201
        return {'message': 'sorry category with name {} already exists'.format(category_name)}, 400

    def get(self):
        categories = category_model.get_all_available_categories()
        if categories:
            return {'categories': categories}, 200
        return {'categories': 'sorry, no categories exist in the database'}, 400


""" Retrieve, Update and delete a category given its id """


@api.route('/category/<int:categoryId>')
class Category (Resource):

    def get(self, categoryId):
        category = category_model.return_category_info_given_Id(categoryId)
        if not category:
            return {'category': 'sorry category with id {} does not exist'.format(categoryId)}, 400
        return {'category': category}, 200

    @api.doc(params=Authorization, required=True)
    @is_admin
    @api.expect(update_info)
    def put(self, categoryId):
        update_data = api.payload
        category_name = update_data['name'].strip().capitalize()
        description = update_data['description']
        response = category_model.update_category(
            categoryId, category_name, description)
        if not response:
            return {'message': 'sorry category with Id {} does not exist'.format(categoryId)}, 400
        if response == 'category name exists':
            return {'message': 'sorry category name {} already exist'.format(category_name)}, 400
        return {'message': 'category info successfully updated'}, 200

    @api.doc(params=Authorization, required=True)
    @is_admin
    def delete(self, categoryId):
        response = category_model.delete_category_by_Id(categoryId)
        if not response:
            return {'message': 'sorry category with Id {} doesnot exist'.format(categoryId)}, 400
        return {'message': 'category with Id {} has been deleted'.format(categoryId)}, 200
