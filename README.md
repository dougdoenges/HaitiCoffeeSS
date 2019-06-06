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
  
## "account/register/"
### GET
  Returns form to create an account
  
### POST
  Creates a user with specified details
  
## "account/signout/"
## GET
  Logs the current user out "/"
  
## "account/myaddress/"
### GET
  Returns all the current users addresses with the user profile in Array

## "account/address/create/"
### GET
  Gets form to create a new address

### POST
  Post a new address

## "account/address/delete/"
### GET
  Gets form to delete an address
  
### POST
  Delete a new address for the user
  
## account/address/edit/<int: addressID>
### GET
  Gets form to edit an existing address
  
### POST
  Updates the address and redirects to "account/address/"
  
## "collections/<int:collection_id>/"
### GET
  Gets all products in the specified collection and returns a page displaying them as well as links to the other collections.
  
## "products/<int:product_id>/"
### GET
  Returns the product details and renders them on a product page.
  
  
## "products/<int:product_id>/order"
### GET
  When the user clicks "BUY" button, create a new order and get all orders made by the user






  
