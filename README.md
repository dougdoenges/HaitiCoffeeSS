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

# manage-site/
  All of the "manage-site/" endpoints are only accessible if the user is an admin

## manage-site/
### GET
  Returns the manage Home page.
  
## manage-site/products/
### GET
  Returns the management page for products.
  
## manage-site/products/create/
### GET
  Returns the form to create a product on a web page.
### POST
  Posts the form to create a new product.
  
## manage-site/products/<int:product_id>/
### GET
  Returns a page with product details and a form to update the product details.
### POST
  Posts the form to update the product details.

## manage-site/products/<int:product_id>/delete/
### GET
  Deletes the product.
  
## manage-site/products/<int:product_id>/images/
### GET
  Returns a page showing the product's images and a form to add a new image to the product.
### POST
  Posts the form to add a new image to the product.

## manage-site/products/<int:product_id>/delete/<int:image_id>/
### GET
  Deletes the specified image from the product.
  
## manage-site/collections
### GET
  Returns the page to manage collections for the site.
  
## manage-site/collections/create/
### GET
  Returns a form to create a new collection for the site.
### POST
  Posts the form to create the new collection.
  
## manage-site/collections/create/<int:collection_id>/
### GET
  Returns collection data and a form to update the given collections information.
### POST
  Posts the form to update the collection information.
  
## manage-site/collections/create/<int:collection_id>/delete/
### GET
  Deletes the given collection
  
## manage-site/orders/
### GET
  Returns a page displaying all the orders and a link to go to a specific order to update.
  
## manage-site/orders/<int:order_id>/
### GET
  Displays the order information and a form to update the order status.
### POST
  Updates the order status.

  
  
  
  
