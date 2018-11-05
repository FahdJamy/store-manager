from app import api
from flask_restplus import Resource, fields
from app.db.products import Product
from app.utils.helpers import is_admin, string_validator

product_model = api.model('Product Model', {
    'name': fields.String(description='product name', required=True, min_length=2, max_length=25),
    'category': fields.String(description='product category', required=True, min_length=2, max_length=25),
    'price': fields.Integer(description='Product price', required=True),
    'quantity': fields.Integer(description='Product quantity', required=True)
})
product_update_info = api.model('Product Update Model', {
    'name': fields.String(description='product name', min_length=2),
    'price': fields.Integer(description='Product price'),
    'quantity': fields.Integer(description='Product quantity'),
    'category': fields.String(description='product category', min_length=2, max_length=25)
})
Authorization = {'token_key': {
    'in': 'header',
    'type': 'JWT',
    'description': 'Token is required'
}}
products_model = Product()


""" Includes api endpoints for creating a new product, viewing all available products, updating its information and deleting a product by Id """


@api.route('/products')
class CreateProduct (Resource):

    @api.doc(params=Authorization, required=True)
    @is_admin
    @api.expect(product_model, validate=True)
    def post(self):
        product_data = api.payload
        name = product_data['name'].strip().capitalize()
        category = product_data['category'].strip().capitalize()
        price = product_data['price']
        quantity = product_data['quantity']
        validate_product_name = string_validator(name)
        if validate_product_name == 'special character exists':
            return {'message' : 'sorry product name shouldnt have a special character including ($#@%)'}, 400
        if not validate_product_name:
            return {'message' : 'sorry product name shouldnt be of spaces only'}, 400
        new_product = products_model.create_product(
            name, category, price, quantity)
        if new_product == 'category name {} doesnot exist'.format(category):
            return {'message': new_product}, 400
        if new_product == 'product name already exists':
            return {'message': 'sorry product with name {} already exists'.format(name)}, 400
        return {'message': 'product has been created successfully!!!'}, 201

    def get(self):
        all_products = products_model.get_all_products()
        if all_products:
            return {'Products': all_products}, 200
        return {'Products': 'sorry no products exist in the database yet'}, 400


""" Retrieve, Update and delete a product given its id """


@api.route('/products/<int:productId>')
class Product (Resource):

    def get(self, productId):
        product = products_model.find_product_by_Id(productId)
        if product == 'no result found':
            return {'product': 'sorry product with id {} does not exist'.format(productId)}, 400
        return {'product': product}, 200


    @api.doc(params=Authorization, required=True)
    @is_admin
    @api.expect(product_update_info)
    def put(self, productId):
        product_data = api.payload
        response = products_model.update_product_info(productId, product_data)
        if response == 'category doesnt exist':
            return {'message': 'sorry you cant update a product info with a category that doesnot exist'}, 400
        if response == 'wrong id':
            return {'message': 'sorry product with Id {} does not exist'.format(productId)}, 400
        if response == 'name exists':
            return {'message': 'sorry product name already exist'.format(productId)}, 400
        if response != 'product name exists':
            return {'message': 'product info successfully updated'}, 200
        return {'message': 'sorry product name {} already exist'.format(product_data['name'])}, 400

    @api.doc(params=Authorization, required=True)
    @is_admin
    def delete(self, productId):
        response = products_model.delete_product(productId)
        if response != 'success':
            return {'message': 'sorry product with Id {} doesnot exist'.format(productId)}, 400
        return {'message': 'product with Id {} has been deleted'.format(productId)}, 200
