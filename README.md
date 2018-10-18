## Store Manager

A store manager is a web application that helps a store owner (admin) to track their sales inventory

[![Build Status](https://travis-ci.org/FahdJamy/store-manager.svg?branch=develop)](https://travis-ci.org/FahdJamy/store-manager)

[![Coverage Status](https://coveralls.io/repos/github/FahdJamy/store-manager/badge.svg?branch=develop)](https://coveralls.io/github/FahdJamy/store-manager?branch=develop)

[![Maintainability](https://api.codeclimate.com/v1/badges/436de29cb33a61a7837a/maintainability)](https://codeclimate.com/github/FahdJamy/store-manager/maintainability)

## Project
- To run the project Locally `https://github.com/FahdJamy/store-manager/tree/develop-api-challenge-2`

- To access and use the application's endpoints on Postman, Use the following URL 
https://fahad-store-manager.herokuapp.com/


## Application Features
| EndPoint  | Function |
| ------------- | ------------- |
|POST /products | Create a new product |
|GET /products   | Get all availabe products |
|GET /products/productId | Get a specific product given its ID |
|POST /sales | Create a new sales record |
|GET /sales   | Get all available sale records |
|GET /sale/saleId | Get a specific sale record given its ID |


## Tools Used
- Flask[Python Web Framework]
- Flask-Restplus[Flask extension for Building RestApis]
- Pytest[Testing Framework]

## An example on how to Use the endpoints
1. Creat a new product
- Open postman and perform a POST request on [https://fahad-store-manager.herokuapp.com/api/v1/products]
- Data should be in json format, e.g
	-`{
  "name": "string",
  "category": "string",
  "price": 0,
  "quantity": 0
}`
	-Note that you shouldn't miss out on any field because they are all required for successful creation of a new product
2. Get all available Products
- Perform a GET request on [https://fahad-store-manager.herokuapp.com/api/v1/products]
3. Get a specific product given its ID
- Perform a GET request and Add an ID for a specific product at the end of this URL say [https://fahad-store-manager.herokuapp.com/api/v1/products/1]
- Note that it will return a message for a product ID that doesn't exist

## Acknowledgments
- `Used this URL as a guideline to build the api endpoints` https://flask-restplus.readthedocs.io/en/stable/

## Authors
- Asiimwe Fahad