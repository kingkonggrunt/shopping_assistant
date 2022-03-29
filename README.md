# Shopping Assistant

## 2022-03-29
Project is halted (for now). It is not possible to scrap products from Coles
as the products as not accessible through BeautifulSoup. I believe the the website hides the products until they need to be rendered in a webbrowser. A solution would be to save rendered html using selenium and perform webscraping from there 

### Objective
To create a Flask API that makes calls to Aldi, Coles, and Woolworths (and other grocery stores). This API will assist a shopper to make purchasing decisions

### List of Behavioral Features
- Search Product Items from a Store/s (find me milk from coles)
- Search Product Items on sale from a store (find me the cheapest milk from Coles)
- Compare prices for a product between stores (which store has the cheapest milk 2l?)
- Users can create a shopping list of items (add "this item" to my shopping list)
- Calculate shopping list cost (by store, by cheapest)

### Todo
- FaskAPI running
- Deployment on remote server
- Search Products from Coles
- View Possible Aldi API

