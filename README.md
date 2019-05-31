# HaitiCoffeeSS

# Server Side Final Project

"/"
### GET:
  returns the index page of the website.
  
  
"account/login/"
### GET
  Returns form to login
  
### POST
  Logs user into the application and takes them to the homepage "/"
  
"account/register/"
### GET
  Returns form to create an account
  
### POST
  Creates a user with specified details
  
"account/logout/"
## GET
  Logs the current user out and takes them to the homepage "/"
  
"account/address/"
### GET
  Returns address management page including all the current users addresses
  
### DELETE
  Deletes an existing address and returns to "account/address/"
  
"account/address/create/"
### GET
  Gets form to create a new address
  
### POST
  Creates a new address for the user and redirects to "account/address/"
  
/account/address/edit/"
### GET
  Gets form to edit an existing address
  
### PATCH
  Updates the address and redirects to "account/address/"
  
"collections/<str:collection-name>/"
### GET
  Gets all products in the specified collection and returns a page displaying them as well as links to the other collections.
  
"products/<str:product-name>/"
### GET
  Returns the product details and renders them on a product page.
  
"cart/add/<str:product-name>/"
### POST
  Adds a given product to the current users cart.

"cart/"
### GET
  Displays the current users cart.
  
### PATCH
  Updates a given product quantity in the cart.
 
### DELETE
  Deletes a given product from the cart and refreshes the "cart/" page
  
"pages/" make all pages these (they just show flat html pages)
  
admin access stuff

  
