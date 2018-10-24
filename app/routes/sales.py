from app import app, api
from flask_restplus import Resource, fields
from app.models.sales import Sale

sale_model = api.model('Sale', {
    'name': fields.String(description='product name', required=True, min_length=5),
    'category': fields.String(description='product category', required=True, min_length=5),
    'price': fields.Integer(description='Product price', required=True),
    'quantity': fields.Integer(description='Quantity', required=True)
})
sales_model = Sale()

""" Create a sales record by sales attndant """


@api.route('/sales')
class Sales (Resource):
    @api.expect(sale_model, validate=True)
    def post(self):
        product_data = api.payload
        new_sales_record = sales_model.create_new_sale_record(product_data)
        return {'Sales record': new_sales_record}, 201

    def get(self):
        all_sales = sales_model.all_sales()
        if all_sales:
            return {'Sale records': all_sales}
        return {'message': 'sorry no records exist yet'}

""" Get a sales record by sales ID """

@api.route('/sale/<int:saleId>')
class Sales (Resource):
    def get(self, saleId):
        sale_record = sales_model.get_single_sale(saleId)
        if sale_record:
            return sale_record
        return {'message': 'no sale record of id {} exists'.format(saleId)}, 400
