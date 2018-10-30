from app import api
from flask_restplus import Resource, fields
from app.db.categories import Category
from app.utils.helpers import is_admin

category_info = api.model('Category', {
    'name': fields.String(description='category name', required=True, min_length=2),
    'description': fields.String(description='category description', required=True, min_length=2)
})
Authorization = {'token_key': {
    'in': 'header',
    'type': 'JWT',
            'description': 'Token is required'
}}
category_model = Category()


""" Class for creating a new category, updating its information and deleting it """


@api.route('/categories')
class Category (Resource):

    @is_admin
    @api.expect(category_info, validate=True)
    def post(self):
        category_data = api.payload
        category_name = category_data['name'].strip().capitalize()
        description = category_data['description']
        new_category = category_model.create_category(
            category_name, description)
        if new_category == 'category created successfully':
            return {'message': 'category has been successfully created !!!'}, 201
        return {'message': 'sorry category with name {} already exists'.format(category_name)}, 400

    def get(self):
        categories = category_model.get_all_available_categories()
        if categories:
            return {'categories': categories}, 200
        return {'message': 'sorry, no categories exist in the database'}, 400
