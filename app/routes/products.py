from app import api
from flask_restplus import Resource, fields
from app.db.products import Product
from app.utils.helpers import is_admin

product_model = api.model('Product Model', {
    'name': fields.String(description='product name', required=True, min_length=2),
    'category': fields.String(description='product category', required=True, min_length=2),
    'price': fields.Integer(description='Product price', required=True),
    'quantity': fields.Integer(description='Product quantity', required=True)
})
product_update_info = api.model('Product Update Model', {
    'name': fields.String(description='product name', min_length=2),
    'price': fields.Integer(description='Product price'),
    'quantity': fields.Integer(description='Product quantity')
})
Authorization = {'token_key': {
    'in': 'header',
    'type': 'JWT',
    'description': 'Token is required'
}}
products_model = Product()


""" Class for creating a new product, updating its information and deleting it """


@api.route('/products')
class Products (Resource):

    @api.doc(params=Authorization, required=True)
    @is_admin
    @api.expect(product_model, validate=True)
    def post(self):
        product_data = api.payload
        name = product_data['name'].strip().capitalize()
        category = product_data['category'].strip().capitalize()
        price = product_data['price']
        quantity = product_data['quantity']
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
        return {'message': 'sorry no products exist yet'}, 400


""" Retrieve, Update and delete a product given its id """


@api.route('/products/<int:productId>')
class Products (Resource):

    def get(self, productId):
        product = products_model.find_product_by_Id(productId)
        if product == 'no result found':
            return {'message': 'sorry product with id {} does not exist'.format(productId)}, 400
        return {'product': product}, 200

    @api.doc(params=Authorization, required=True)
    @is_admin
    @api.expect(product_update_info)
    def put(self, productId):
        product_data = api.payload
        response = products_model.update_product_info(productId, product_data)
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
