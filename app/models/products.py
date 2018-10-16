class Products:

	def __init__(self):
		self.products = []
		self.pdt_id = 0

	def create_new_product(self, pdt_name, category, price):
		_id = self.pdt_id =+ 1
		new_product = {
			"id" : _id,
			"name" : pdt_name,
			"price" : price,
			"category" : category
		}
		self.products.append(new_product)
		return new_product

	def find_product_by_id(self, _id):
		product = next(filter(lambda x: x['id'] == _id, self.products), None)
		if product:
			return product

	def return_all_product(self):
		if len(self.products) > 0 :
			result = [pdt for pdt in self.products]
			return result

	def delete_products(self):
		if len(self.products) > 0:
			for  x in self.products:
				self.products.remove(self.products[x])