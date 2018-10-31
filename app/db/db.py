import psycopg2
import os
from app import app
from psycopg2.extras import RealDictCursor


class DB:
    def __init__(self):
        """ Connect to the database """
        self.database = app.config['DATABASE']
        if os.getenv('DEPLOY'):
            self.database = os.getenv('DEPLOY_DATABASE')
        try:
            self.conn = psycopg2.connect(self.database)
            print("successfully connected")
            self.cur = self.conn.cursor()
            self.conn.autocommit = True
        except (Exception, psycopg2.DatabaseError) as e:
            print(e, "Can't connect to the db")

        self.create_tables()

    """ Method to create tables """

    def create_tables(self):
        """ Sql statements for creating the table (users, products, sales,categories) """
        create_table_sql_queries = (
            """
            CREATE TABLE IF NOT EXISTS users (
                id serial,
                username VARCHAR(25) UNIQUE NOT NULL,
                password VARCHAR(100) NOT NULL,
                admin boolean default false,
                PRIMARY KEY (id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS categories (
                id serial,
                category_name VARCHAR(500) UNIQUE NOT NULL,
                description VARCHAR(100) NOT NULL,
                PRIMARY KEY (category_name)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                id serial,
                product_name VARCHAR(100) UNIQUE NOT NULL,
                category VARCHAR(100) NOT NULL,
                price int not null,
                stock int not null,
                PRIMARY KEY (product_name),
                FOREIGN KEY (category) REFERENCES categories(category_name) ON DELETE CASCADE

            );
            """,
            """
            CREATE TABLE IF NOT EXISTS sales (
                id serial,
                product_name VARCHAR(100) NOT NULL,
                category VARCHAR(100) NOT NULL,
                price int not null,
                quantity int not null,
                total_amount int not null,
                created_by VARCHAR(100) NOT NULL,
                created_on VARCHAR(100) NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (product_name) REFERENCES products(product_name) ON DELETE CASCADE
            );
            """
        )

        for query in create_table_sql_queries:
            self.cur.execute(query)
            self.conn.commit()

    """ Method to drop tables """

    def drop_tables(self, *tables):
        for table in tables:
            query = 'DROP TABLE IF EXISTS {}'.format(table)
            self.cur.execute(query)
            self.conn.commit()

    """ Method executes a query statement """

    def execute_query(self, query):
        try:
            self.cur.execute(query)
            self.conn.commit()
            return ('success')
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
            return None

    """ Return one value (dictionaries)."""

    def fetch_one(self, query_param):
        try:
            self.dict_cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.dict_cur.execute(query_param)
            result = self.dict_cur.fetchone()
            if result:
                return result
            return ('no result found')
        except (Exception, psycopg2.DatabaseError) as e:
            print(e, 'None')
            return None

    """ Return all values (dictionaries)."""

    def fetch_all(self, query_param):
        try:
            self.dict_cur = self.conn.cursor(cursor_factory=RealDictCursor)
            self.dict_cur.execute(query_param)
            results = self.dict_cur.fetchall()
            if results:
                return results
        except (Exception, psycopg2.DatabaseError) as e:
            print(e, 'None')
            return None
