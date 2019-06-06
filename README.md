# HaitiCoffeeSS

# Server Side Final Project

## "/"
### GET:
  returns the index page of the website.
  
  
## "account/signin/"
### GET
  Returns form to login
  
### POST
  Logs user into the application and takes them to the homepage "/"
  
### Error Handling:
  1. If the user is already signin, Response "You are already signed in"
  2. If the user types the wrong account/password, Response "Invalid credentials"
  3. If the user access with the wrong request method, Response "Bad Login Form"
  
## "account/register/"
### GET
  Returns form to create an account
  
### POST
  Creates a user with specified details
  
### Error Handling:
  1. If the password and password confirmation do not match, response "Password did not match"
  2. If the user types the wrong account/password, Response "Invalid Registration Request"
  3. If the user access with the wrong request method, Response "Method not allowed"
  
  
## "account/signout/"
### GET
  Logs the current user out "/"
  
### Error Handling:
  1. If the user is not logged in and try to sign out, response "Not logged In"
  2. If the user access with the wrong request method, Response "Method not allowed" 
  
  
## "account/myaddress/"
### GET
  Returns all the current users addresses with the user profile in Array
  
### Error Handling:
  JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
  BadRequestMessage = "Bad request."
  DatabaseErrorMessage = "Error interacting with database."

## "account/address/create/"
### GET
  Gets form to create a new address

### POST
  Post a new address
  
### Error Handling:
  JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
  BadRequestMessage = "Bad request."
  DatabaseErrorMessage = "Error interacting with database."
  

## "account/address/delete/"
### GET
  Gets form to delete an address
  
### POST
  Delete a new address for the user
  
### Error Handling:
  JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
  BadRequestMessage = "Bad request."
  DatabaseErrorMessage = "Error interacting with database."
  Method not allowed for the wrong request method
  
## account/address/edit/<int: addressID>
### GET
  Gets form to edit an existing address
  
### POST
  Updates the address and redirects to "account/address/"
  
### Error Handling:
  If the user trys to change the wrong address, response You may only edit your own address
  JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
  BadRequestMessage = "Bad request."
  DatabaseErrorMessage = "Error interacting with database."  
  Method not allowed for the wrong request method
  
## "collections/<int:collection_id>/"
### GET
  Gets all products in the specified collection and returns a page displaying them as well as links to the other collections.

### Error Handling:
  JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
  BadRequestMessage = "Bad request."
  DatabaseErrorMessage = "Error interacting with database."
  
  
## "products/"
### GET 
  Get all Products as array
  
### Error Handling:
  JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
  BadRequestMessage = "Bad request."
  DatabaseErrorMessage = "Error interacting with database."
  Method not allowed for the wrong request method
  

## "products/<int:product_id>/"
### GET
  Returns the product details and renders them on a product page.
  
### Error Handling:
  JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
  BadRequestMessage = "Bad request."
  DatabaseErrorMessage = "Error interacting with database."
  Method not allowed for the wrong request method
  
## "products/<int:product_id>/purchase"
### GET
  When the user clicks "BUY" button, create a new order and get all orders made by the user
  
### Error Handling:
  JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
  BadRequestMessage = "Bad request."
  DatabaseErrorMessage = "Error interacting with database."
  Method not allowed for the wrong request method






  
