from app import app, api
from flask_restplus import Resource, fields
from app.models.sales import Sales

sale_model = api.model('Product', {
		'name' : fields.String(description='product name', required=True, min_length=5),
		'category' : fields.String(description='product category', required=True, min_length=5),
		'price' : fields.Integer(description='Product price', required=True),
		'quantity' : fields.Integer(description='Quantity', required=True)
	})
sales_model = Sales ()

""" Create a sales record by sales attndant """
@api.route('/sales')
class Sales (Resource):
	@api.expect(sale_model, validate=True)
	def post(self):
		product_data = api.payload
		name = product_data['name']
		category = product_data['category']
		price = product_data['price']
		quantity = product_data['quantity']
		username = 'mags'
		new_sales_record = sales_model.create_new_sale_record(name, price, category, quantity, username)
		return {'Sales record' : new_sales_record}, 201

	def get(self):
		all_sales = sales_model.all_sales()
		if all_sales:
			return {'Sale records' : all_sales}
		return {'message' : 'sorry no records exist yet'}