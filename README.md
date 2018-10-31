## Store Manager - Challenge 3

[![Build Status](https://travis-ci.org/FahdJamy/store-manager.svg?branch=develop-api-challenge-3)](https://travis-ci.org/FahdJamy/store-manager)

[![Coverage Status](https://coveralls.io/repos/github/FahdJamy/store-manager/badge.svg?branch=develop-api-challenge-3)](https://coveralls.io/github/FahdJamy/store-manager?branch=develop-api-challenge-3)

[![Maintainability](https://api.codeclimate.com/v1/badges/436de29cb33a61a7837a/maintainability)](https://codeclimate.com/github/FahdJamy/store-manager/maintainability)

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