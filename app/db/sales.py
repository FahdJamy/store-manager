from datetime import datetime
from app.db.db import DB
from app.db.categories import Category
from app.db.products import Product


class Sale:
    def __init__(self):
        self.db_handler = DB()
        self.product_handler = Product()

    """ Creates a new sales record but first check if the product already exists"""

    def create_sales_record(self, name, quantity, created_by):
        response = self.product_handler.find_product_by_name(name)
        if response != "no result found":
            price = response['price']
            category = response['category']
            current_stock = response['stock']
            if current_stock == 0:
                return "out of stock"
            if current_stock < quantity:
                return "cant make sale, current_stock is less than provided quantity"
            total_amount = price * quantity
            date_created = str((datetime.utcnow()).strftime('%d %b,%Y'))
            insert_sql = "INSERT INTO sales (product_name,category,price,quantity,total_amount,created_by, created_on) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                name, category, price, quantity, total_amount, created_by, date_created)
            result = self.db_handler.execute_query(insert_sql)
            remaining_stock = current_stock - quantity
            data = {'name': name, 'price': price,
                    'quantity': int(remaining_stock)}
            self.product_handler.update_product_info(1, data)
            return "success"

    """ Delete a sale record """

    def delete_sales_record(self, sale_id):
        existing_sale = self.find_sale_by_Id(sale_id)
        if existing_sale == 'no result found':
            return 'no record'
        delete_query = f"DELETE FROM sales WHERE id = '{sale_id}'"
        response = self.db_handler.execute_query(delete_query)
        return response

    """ find sale record by its Id """

    def find_sale_by_Id(self, _id):
        find_sql_query = "SELECT * FROM sales WHERE id = '{}'".format(_id)
        sale_record = self.db_handler.fetch_one(find_sql_query)
        return sale_record

    """ Return all sales records """

    def get_all_sale_records(self):
        all_sales_query = "SELECT * FROM sales"
        sales = self.db_handler.fetch_all(all_sales_query)
        return sales

    """ Get user sale records"""

    def get_user_records(self, username):
        get_sale_query = "SELECT * FROM sales WHERE created_by = '{}'".format(
            username)
        user_sale_records = self.db_handler.fetch_all(get_sale_query)
        return user_sale_records
