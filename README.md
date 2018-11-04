## Store Manager - Challenge 3

#### A store manager is a web application that helps a store owner (admin) to track their sales inventory

[![Build Status](https://travis-ci.org/FahdJamy/store-manager.svg?branch=develop-api-challenge-3)](https://travis-ci.org/FahdJamy/store-manager)

[![Coverage Status](https://coveralls.io/repos/github/FahdJamy/store-manager/badge.svg?branch=develop-api-challenge-3)](https://coveralls.io/github/FahdJamy/store-manager?branch=develop-api-challenge-3)

[![Maintainability](https://api.codeclimate.com/v1/badges/436de29cb33a61a7837a/maintainability)](https://codeclimate.com/github/FahdJamy/store-manager/maintainability)

## Project
- To run the project Locally, clone `https://github.com/FahdJamy/store-manager/tree/develop-api-challenge-3`
	1. cd into the folder that contains the cloned project.
	2. create a virtual environment.
	3. activate the virtual environment.
	4. pip install the requirements.txt.
	5. to run the project use python3. the run command is [python run.py].

- Checkout the live demo on this URL: https://store-manager-challenge-3.herokuapp.com/

# Functionality
- Admin creates an account for a sales attendant. 
- Admin can give admin right to sales attendant.
- Create new product.
- Modify product.
- Update product details. 
- Delete product.
- Get all available products.
- Create catefory.
- Modify catefory.
- Delete category.
- Get all categories.
- Get a specific Category.
- Create a sales record.
- Get a specific sales record.
- Get all sales records for user.
- Get all sales records.

# Dependencies Used
- Flask(python web framework )
- Flask_Restplus(flask framework for building APis)
- Pytest(Testing Framework)
- pyjwt(Json Web Token authentication library)
- Postgres(Database)

# Api End Points 
| EndPoint  | Function | Acessed by |
| ------------- | ------------- | ------------- |
|`POST /auth/signup`  | create a user account | admin |
|`POST /auth/login` | Verify a user and create token | sales attendant and admin |
|`PUT /users/<userId> `| Give sales attendant admin right | only admin |
|`POST /products  ` | Create Product | admin |
|`GET /products `         | Get all products | sales attendant and admin |
|`GET /products/<productId> ` | Get single product by Id | sales attendant and admin |
|`PUT /products/<productId> `  | Update product info | admin |
|`DELETE /products/<productId>`  | delete product by Id| admin |
|`GET /categories`  | view available categories | sales attendant and admin |
|`GET /category/<categoryId>`  | view specific category | sales attendant and admin |
|`POST /categories`       | Create new category | admin |
|`PUT /category/<categoryId>` | Modify category | admin |
|`DELETE /category/<categoryId>` | Delete category | admin |
|`POST /sales` | Create new sales record | sale attendant |
|`GET /sales` | View all sale records | sale record creator and admin |
|`GET /sales/<saleId>` | Get specific sales record | sale record creator and admin |
|`DELETE /sales/<saleId>` | Delete sales record | admin |

Note 
- admin = Store owner
- prefix to the endpoints = /api/v2
- a default super user is created by default. (username = "admin" and password = "123")


# Database Structure
### users.
|column name|type|
|-----------------|---------------|
|id|int(primary key,unique)|
|username|character(unique)|
|password|characters|
|admin|boolen|

### categories.
|column name|type|
|--------------------|--------------------|
|id|int(primary key,unique)|
|category_name|varchar(unique)|
|description|varchar()

### products.
|column name|type|
|--------------------|--------------------|
|id|int(unique)|
|product_name|varchar(unique) primary key|
|category|varchar(unique)fk(references category_name)|
|price|int|
|stock|int|

### sales.
|column name|type|
|--------------------|--------------------|
|id|int(unique) primary key|
|product_name|varchar(unique) fk(references product_name)|
|category|varchar(unique)|
|quantity|int|
|total_amount|int|
|created_by|varchar()|
|created_on|varchar()|

## Developed by
- Asiimwe Fahad