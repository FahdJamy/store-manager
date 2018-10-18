class Sales:
	def __init__(self):
		self.sales = []
		self.sale_id = 0
		self.result = []

	def create_new_sale_record(self, pdt_name, price, category, quantity, username):
		_id = self.sale_id =+ 1
		total = price * quantity
		new_sales_record = {
			"id" : _id,
			"product_name" : pdt_name,
			"price" : price,
			"category" : category,
			"quantity" : quantity,
			"total_amount" : total,
			"created_by" : username
		}
		self.sales.append(new_sales_record)
		return new_sales_record

	def all_sales(self):
		if len(self.sales) > 0:
			return self.sales

	def all_sales_by_user(self, username):
		for r in self.sales:
			if r['created_by'] == username:
				self.result.append(r)
		if len(self.result) > 0:
			return self.result

	def get_single_sale(self, _id):
		for p in self.sales:
			if p['id'] == _id:
				self.result.append(p)
		if len(self.result) > 0:
			return self.result