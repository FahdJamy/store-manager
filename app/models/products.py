""" Product model class represents methods for creating a new product """


class Product:

    def __init__(self):
        self.products = []
        self.pdt_id = 0

    """ Create a new product given a product name, category and price. """

    def create_new_product(self, pdt_name, category, price):
        check_name = self.find_product_by_name(pdt_name)
        if check_name == 'exists':
            return ('sorry product name ({}) already exists'.format(pdt_name))
        self.pdt_id = self.pdt_id + 1
        new_product = {
            "id": self.pdt_id,
            "name": pdt_name,
            "price": price,
            "category": category
        }
        self.products.append(new_product)
        return new_product

    """ Find and return a specific product given it's ID """

    def find_product_by_id(self, _id):
        product = next(filter(lambda x: x['id'] == _id, self.products), None)
        if product:
            return product

    """ find product by name."""
    def find_product_by_name(self, pdt_name):
        if len(self.products) > 0:
            for product in self.products:
                if product['name'] == pdt_name:
                    return ('exists')


    """ Return all available products. """

    def return_all_product(self):
        if len(self.products) > 0:
            result = [pdt for pdt in self.products]
            return result

    """ Delete all available products."""

    def delete_products(self):
        if len(self.products) > 0:  # check if the list length is greater than 0
            for x in self.products:
                self.products.remove(self.products[x])
