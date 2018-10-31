from app.db.db import DB
from .categories import Category


class Product:
    def __init__(self):
        self.db_handler = DB()
        self.category_handler = Category()

    """ Creates a new product but first check if the name passed doesnot exist"""

    def create_product(self, name, category, price, stock):
        response = self.find_product_by_name(name)
        if response == "no result found":
            category_name = self.category_handler.find_category_by_name(category)
            if category_name == 'no result found':
                return 'category name {} doesnot exist'.format(category)
            insert_sql = "INSERT INTO products (product_name, category, price, stock) VALUES ('{}', '{}', '{}', '{}')".format(
                name, category, price, stock)
            result = self.db_handler.execute_query(insert_sql)
            return 'product created successfully'
        return 'product name already exists'

    """ Update a product details """

    def update_product_info(self, _id, data):
        product_response = self.find_product_by_Id(_id)
        if product_response == 'no result found':
            return 'wrong id'
        name = data['name'].strip().capitalize()
        price = data['price']
        quantity = data['quantity']
        if price != 0:
            update_price = "UPDATE products SET price = '{}' WHERE id = '{}'".format(price, _id)
            self.db_handler.execute_query(update_price)
        if quantity != 0:
            update_quantity = "UPDATE products SET stock = '{}' WHERE id = '{}'".format(quantity, _id)
            self.db_handler.execute_query(update_quantity)
        if name != "":
            existing_name = self.find_product_by_name(name)
            if existing_name != 'no result found':
                return 'name exists'
            if existing_name == "no result found":
                update_product_name = "UPDATE products SET product_name = '{}' WHERE id = '{}'".format(name, _id)
                self.db_handler.execute_query(update_product_name)
        return 'product info updated'

    """ Delete a product """
    def delete_product(self, _id):
        response = self.find_product_by_Id(_id)
        if response != 'no result found':
            delete_query = f"DELETE FROM products WHERE id = '{_id}'"
            response = self.db_handler.execute_query(delete_query)
            return response

    """ find product by its name """

    def find_product_by_name(self, name):
        find_query = f"SELECT * FROM products WHERE product_name = '{name}'"
        product = self.db_handler.fetch_one(find_query)
        return product

    def find_product_by_Id(self, _id):
        find_query = f"SELECT * FROM products WHERE id = '{_id}'"
        response = self.db_handler.fetch_one(find_query)
        return response

    """ Return all products """

    def get_all_products(self):
        all_products_query = "SELECT * FROM products"
        products = self.db_handler.fetch_all(all_products_query)
        return products


# user = Users()
# new_user = user.create_user('man', 'weed')
