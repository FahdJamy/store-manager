from app import api
from flask_restplus import Resource, fields
from app.db.sales import Sale
from app.utils.helpers import token_required, is_admin, user_from_token

sale_model = api.model('Sales', {
    'name': fields.String(description='product name', required=True, min_length=2),
    'quantity': fields.Integer(description='quantity', required=True)
})
Authorization = {'token_key': {
    'in': 'header',
    'type': 'JWT',
    'description': 'Token is required'
}}
sales_model = Sale()

""" Create a sales record by sales attndant """


@api.route('/sales')
class Sales (Resource):
    @api.doc(params=Authorization, required=True)
    @token_required
    @api.expect(sale_model, validate=True)
    def post(self):
        product_data = api.payload
        name = product_data['name'].strip().capitalize()
        quantity = product_data['quantity']
        user = user_from_token()
        if user['admin']:
            return {'message': 'sorry an admin cant create a sales record'}, 401
        username = user['username']
        new_sales_record = sales_model.create_sales_record(
            name, quantity, username)
        if not new_sales_record:
            return {'message': 'sorry cant make a sale record of a product that doesnt exist in the db'}, 400
        if new_sales_record == 'out of stock':
            return {'message': 'sorry, product is out of stock'}, 400
        if new_sales_record == 'cant make sale, current_stock is less than provided quantity':
            return {'message': new_sales_record}
        return {'message': 'sale record created'}, 201