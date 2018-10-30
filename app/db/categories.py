from app.db.db import DB


class Category:
    def __init__(self):
        self.db_handler = DB()

    """ Creates a new product but first check if the name passed doesnot exist"""

    def create_category(self, name, description):
        response = self.find_category_by_name(name)
        if response == "no result found":
            insert_sql = "INSERT INTO categories (category_name, description) VALUES ('{}', '{}')".format(name, description)
            result = self.db_handler.execute_query(insert_sql)
            return 'category created successfully'
        return 'cateogry name already exists'


    def find_category_by_name(self, name):
        find_query = f"SELECT * FROM categories WHERE category_name = '{name}'"
        category = self.db_handler.fetch_one(find_query)
        return category

    def find_category_by_ID(self, _id):
        find_query = f"SELECT * FROM categories WHERE id = '{_id}'"
        category = self.db_handler.fetch_one(find_query)
        return category

    def get_all_available_categories(self):
        sql_query = "SELECT * FROM categories"
        categories = self.db_handler.fetch_all(sql_query)
        return categories

    def delete_category_by_Id(self, category_Id):
        response = self.find_category_by_ID(category_Id)
        if response != 'no result found':
            delete_query = f"DELETE FROM categories WHERE id = '{category_Id}'"
            self.db_handler.execute_query(delete_query)
            return 'category deleted'

    def return_category_info_given_Id(self, category_id):
        response = self.find_category_by_ID(category_id)
        if response != 'no result found':
            select_query = f"SELECT * FROM categories WHERE id = '{category_id}'"
            category = self.db_handler.fetch_one(select_query)
            return category

    def update_category(self, _id, name=None, description=None):
        response = self.find_category_by_ID(_id)
        if response != 'no result found':
            if description:
                update_query = "UPDATE categories SET description = '{}' WHERE id = '{}'".format(description, _id)
                self.db_handler.execute_query(update_query)
            if name:
                existing_name = self.find_category_by_name(name)
                if existing_name != "no result found":
                    return 'category name exists'
                update_query = "UPDATE categories SET category_name = '{}' WHERE id = '{}'".format(name, _id)
                self.db_handler.execute_query(update_query)
            return 'category info successfully updated'