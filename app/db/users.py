from app.db.db import DB
from app import app
import os


class User:
    def __init__(self):
        self.db_handler = DB()
        self.create_admin()

    """ Creates a new user """

    def create_user(self, _name, _passcode):
        if not _name or not _passcode:
            print('sorry you missing a parameter')
        resp = self.find_user_by_username(_name)
        if resp == "no result found":
            insert_sql = "INSERT INTO users (username, password) VALUES ('{}', '{}')".format(
                _name, _passcode)
            result = self.db_handler.execute_query(insert_sql)
            return result
        return ('sorry username {} is already taken'.format(_name))

    def update_user_info(self, user_id, admin_v):
        response = self.find_user_by_Id(user_id)
        if response != 'no result found':
            update_query = "UPDATE users SET admin = '{}' WHERE id = '{}'".format(
                admin_v, user_id)
            update_response = self.db_handler.execute_query(update_query)
            return update_response
        return ('user with id {} is not found'.format(user_id))

    def delete_user(self, username):
        delete_query = f"DELETE FROM users WHERE username = '{username}'"
        response = self.db_handler.execute_query(delete_query)
        return response

    def find_user_by_username(self, username):
        find_query = f"SELECT * FROM users WHERE username = '{username}'"
        user = self.db_handler.fetch_one(find_query)
        return user

    def find_user_by_Id(self, user_id):
        find_query = f"SELECT * FROM users WHERE id = '{user_id}'"
        user = self.db_handler.fetch_one(find_query)
        return user

    def get_all_users(self):
        all_users_query = "SELECT * FROM users"
        users = self.db_handler.fetch_all(all_users_query)
        return users

    def verify_username_and_password(self, username, _password):
        response = self.find_user_by_username(username)
        if response == 'no result found':
            return 'no user'
        for detail in response:
            if response[detail] == _password:
                return 'success'

    """ method to only create a default admin when not runninf tests"""

    def create_admin(self):
        if os.getenv('CONFIG_NAME') != 'testing':
            admin_response = self.find_user_by_username('admin')
            if admin_response == 'no result found':
                response = self.create_user('Admin', '123')
                if response == 'success':
                    self.update_user_info(1, True)
                    return 'admin created'
