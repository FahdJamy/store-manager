from app import app, api
from flask_restplus import Resource, fields
from app.models.products import Products

product_model = api.model('Product', {
    'name': fields.String(description='product name', required=True, min_length=5),
    'category': fields.String(description='product category', required=True, min_length=5),
    'price': fields.Integer(description='Product price', required=True)
})
products_model = Products()


""" Create a sales attendant """


@api.route('/products')
class Users (Resource):

    @api.expect(product_model, validate=True)
    def post(self):
        user_data = api.payload
        name = user_data['name']
        category = user_data['category']
        price = user_data['price']
        new_product = products_model.create_new_product(name, category, price)
        return {'product': new_product}, 201