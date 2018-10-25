from app import app, api
from flask_restplus import Resource, fields
from app.models.products import Product

product_model = api.model('Product', {
    'name': fields.String(description='product name', required=True, min_length=5),
    'category': fields.String(description='product category', required=True, min_length=5),
    'price': fields.Integer(description='Product price', required=True)
})
products_model = Product()


""" Create a new product and return all available products """


@api.route('/products')
class Products (Resource):

    @api.expect(product_model, validate=True)  # create a new product
    def post(self):
        user_data = api.payload
        name = (user_data['name']).strip()
        category = (user_data['category']).strip()
        price = user_data['price']
        new_product = products_model.create_new_product(name, category, price)
        return {'product': new_product}, 201

    def get(self):  # Return all available products
        all_products = products_model.return_all_product()
        if all_products:
            return {'Products': all_products}
        return {'message': 'sorry no products exist yet'}


""" Return a specific product given its id """


@api.route('/products/<int:productId>')
class Products (Resource):

    def get(self, productId):
        product = products_model.find_product_by_id(productId)
        if product:
            return product
        return {'message': 'sorry product with id {} doesnot exist'.format(productId)}, 400
