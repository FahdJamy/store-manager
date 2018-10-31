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
        new_product = products_model.create_product(name, category, price, quantity)
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