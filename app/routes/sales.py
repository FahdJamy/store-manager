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

    @api.doc(params=Authorization, required=True)
    @token_required
    def get(self):
        user = user_from_token()
        if user['admin']:
            available_sale_records = sales_model.get_all_sale_records()
            if available_sale_records:
                return {'sales': available_sale_records}, 200
        user_sale_records = sales_model.get_user_records(user['username'])
        if user_sale_records:
            return {'records': user_sale_records}, 200
        return {'message': 'sorry no sales records exist in the db yet'}, 400


@api.route('/sales/<int:saleId>')
class Sale (Resource):
    @api.doc(params=Authorization, required=True)
    @token_required
    def get(self, saleId):
        sale_record = sales_model.find_sale_by_Id(saleId)
        user = user_from_token()
        if sale_record != 'no result found' and user['username'] == sale_record['created_by']:
            return {'sale record': sale_record}, 200
        elif sale_record != 'no result found':
            return {'sale record': sale_record}, 200
        return {'message': 'sorry, sale record of id {} doesnot exists'.format(saleId)}, 400
