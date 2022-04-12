import os
from types import CoroutineType

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from src.database import connections
from src.filters import ColesFilter
from src.items import ColesItem
from src.web import FirefoxDriver


load_dotenv()



def coles_item(headless: bool=True, pipe_to: CoroutineType=None) -> str:  #TODO: refactor so that it can accept different urls
    """Send a Search Page result from a shopping website to another coroutine

    Args:
        headless (bool, optional): Run Selenium scraper in headless mode. Defaults to True.
        pipe_to (Generator, optional): Next Coroutine to send page_source to. Defaults to None.
    """

    url = "https://shop.coles.com.au/a/national/everything/search/"

    print(f"Open to Product Searching on : {url}")

    while True:
        search_item = (yield)

        with FirefoxDriver(driver_path="/home/mint/Desktop/Development/shopping_assistant/gecko/geckodriver", headless=headless) as d:
            d.get(f"{url}{search_item}")
            if pipe_to:
                pipe_to.send(d.page_source)


def filter_search_result(item_filter: ColesFilter, pipe_to: CoroutineType=None) -> BeautifulSoup:
    """Filter a Page Source with a SoupStrainer Object

    Args:
        item_filter (ColesFilter): A predefined SoupStrainer object
        pipe_to (Generator, optional): Coroutine to send filtered page source to. Defaults to None.
    """
    print(f"Open for Filtering Page Source Data. Filter: {item_filter}")

    while True:
        page_source: str = (yield)
        soup = BeautifulSoup(page_source, 'html.parser',
                             parse_only=item_filter())

        if pipe_to:
            pipe_to.send(soup)

def identify_coles_products(pipe_to: CoroutineType=None) -> ColesItem:
    """Identify all Coles Products from a page source

    Args:
        pipe_to (Generator, optional): Coroutine to send a ColesItem to. Defaults to None.

    Returns:
        ColesItem: ColesItem DataClass
    """

    print("Open for Identifying Coles Product")

    while True:
        soup: BeautifulSoup = (yield)

        for header in soup.find_all("header", class_="product-header"):
            # item = ColesItem(
            #     full_name=header.find('span', class_="accessibility-inline").text,
            #     brand=header.find('span', class_="product-brand").text,
            #     name=header.find('span', class_="product-name").text,
            #     size=header.find('span', class_="package-size").text,
            #     dollar=header.find('span', class_="dollar-value").text,
            #     cent=header.find('span', class_="cent-value").text,
            #     unit_price=header.find('span', class_="package-price").text,
            #     id=header.find("h3", class_="product-title")['data-itemid'],
            #     link=header.find("a", class_="product-image-link")['href'],
            #     partnumber=header.find("h3", class_="product-title")['data-partnumber']
            # )
            item = ColesItem.from_header(header)

            if pipe_to:
                pipe_to.send(item)

def normalize_coles_item(pipe_to: CoroutineType=None) -> dict:
    """Normalize a ColesItem into a dictionary appriopiate for the database

    Args:
        pipe_to (Generator, optional): Coroutine to send dictionary to. Defaults to None.

    Returns:
        dict: Normalized ColesItem
    """

    print("Open for Normalisating ColesItems to Dictionary")

    while True:
        item: ColesItem = (yield)
        # item_dict = item.to_dict()

        # normalize_item = {
        #     "id" : item_dict['id'],
        #     "full_name": item_dict['full_name'],
        #     "brand": item_dict['brand'],
        #     "size": item_dict["size"],
        #     "link": item_dict['link'],
        #     "partnumber" : item_dict['partnumber'],
        #     "price_history": [{
        #         "date": datetime.datetime.utcnow(),
        #         "price": item_dict['price'],
        #         "dollar": item_dict['dollar'],
        #         "cent": item_dict['cent'],
        #         "unit_price": item_dict['unit_price'],
        #         "sale_type": item_dict['sale_type'],
        #     }]
        # }

        if pipe_to:
            pipe_to.send(item.normalize_for_db())

def printer(pipe_to: CoroutineType=None):
    """Printer

    Args:
        pipe_to (Generator, optional): Coroutine to send data to. Defaults to None.
    """
    print("Printer Open")
    while True:
        _ = (yield)
        print(_)
        
        if pipe_to:
            pipe_to.send(_)

def save_to_db(pipe_to: CoroutineType=None) -> str:
    """Save a Dictionary to a database

    Args:
        pipe_to (Generator, optional): Coroutine to send database response to. Defaults to None.

    Returns:
        str: Database Response
            On insert_one return the id of the new database entry
            On update_one return the amount of keys that are modified in the database
    """
    # client = MongoClient(os.environ.get('HOST'),
    #                      username=os.environ.get('USERNAME'),
    #                      password=os.environ.get('PASSWORD'),
    #                      authSource=os.environ.get('AUTHSOURCE'))
    # db = client.test
    # collection = db.coles_item_3

    mongo = connections.Mongo(host=os.environ.get("HOST"),
                              username=os.environ.get('USERNAME'),
                              password=os.environ.get('PASSWORD'),
                              authSource=os.environ.get('AUTHSOURCE'))
    mongo.set_db("test")
    mongo.set_collection("coles_item_3")

    print("Database Open")

    while True:
        item: dict = (yield)

        search_query = {"id": item['id']}
        if result := mongo.collection.find_one(search_query):
            update = dict()
            update['$set'] = dict()
            if result['full_name'] != item['full_name']:
                update['$set']['full_name'] = item['full_name']
            if result['brand'] != item['brand']:
                update['$set']['brand'] = item['brand']
            if result['size'] != item['size']:
                update['$set']['size'] = item['size']

            update["$push"] = {"price_history": item['price_history'][0]}
            _ = mongo.collection.update_one(search_query, update).modified_count
        else:
            _ = mongo.collection.insert_one(item).inserted_id

        if pipe_to:
            pipe_to.send(_)


def main():
    """Main Function
    Run the coroutine pipeline
    """
    p = printer()
    to_db = save_to_db(pipe_to=p)
    normalize = normalize_coles_item(pipe_to=to_db)
    identifier = identify_coles_products(pipe_to=normalize)
    products = filter_search_result(ColesFilter.AllProducts, pipe_to=identifier)
    item_search = coles_item(headless=False, pipe_to=products)

    next(item_search)

    next(products)
    next(identifier)
    next(normalize)
    next(to_db)
    next(p)

    while True:
        item = input("What Coles Item are you looking for? ")
        if item:
            item_search.send(item)
        
            

if __name__ == "__main__":
    main()