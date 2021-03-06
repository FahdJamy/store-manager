""" Sale model class represents methods for creation and retrieval from non-persistent databases of sale records."""


class Sale:
    def __init__(self):
        self.sales = []
        self.sale_id = 0
        self.result = []

    """ Create a new sale record."""

    def create_new_sale_record(self, product_data):
        name = (product_data['name']).strip()
        category = (product_data['category']).strip()
        price = product_data['price']
        quantity = product_data['quantity']
        username = 'mags'

        self.sale_id = self.sale_id + 1
        total = price * quantity
        new_sales_record = {
            "id": self.sale_id,
            "product_name": name,
            "price": price,
            "category": category,
            "quantity": quantity,
            "total_amount": total,
            "created_by": username
        }
        self.sales.append(new_sales_record)
        return new_sales_record

    """ Return all sale records available"""

    def all_sales(self):
        if len(self.sales) > 0:
            return self.sales

    def all_sales_by_user(self, username):
        pass

    """ Get a specific sale record given its ID."""

    def get_single_sale(self, _id):
        for sale_record in self.sales:
            if sale_record['id'] == _id:
                return sale_record
        # if len(self.result) > 0:
        # 	return self.result
