

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


from bs4 import BeautifulSoup, SoupStrainer

from pymongo import MongoClient
import json

import os
from dotenv import load_dotenv

from coles import ColesItem
from filters import ColesFilter

import datetime


load_dotenv()

def get_milk():
    url = "https://shop.coles.com.au/a/national/everything/search/breakfast"

    options = Options()
    # options.headless = True
    driver = webdriver.Firefox(options=options,
                               executable_path=r"/home/mint/Desktop/Development/shopping_assistant/gecko/geckodriver")
    driver.get(url)
    
    with open('stores/coles/breakfast.html', 'w') as f:
        f.write(driver.page_source)

    driver.quit()
    
    
# def coroutine(func):
#     def start(*args,**kwargs):
#         cr = func(*args,**kwargs)
#         cr.next()
#         return cr
#     return start
    
    
class FirefoxDriver:
    def __init__(self, *, headless: bool=True):
        self.options = Options()
        self.options.headless = headless
        self.driver = None
        
    def __enter__(self):
        self.driver = webdriver.Firefox(options=self.options, 
                                        executable_path=r"/home/mint/Desktop/Development/shopping_assistant/gecko/geckodriver")
        return self.driver
    
    def __exit__(self, exc_type, exc_value, exe_traceback):
        self.driver.quit()
    
def coles_item(headless: bool=True, next=None):
    url = "https://shop.coles.com.au/a/national/everything/search/"
    print("Open to Searching for Products")
    while True:
        search_item = (yield)
        
        with FirefoxDriver(headless=False) as d:
            d.get(f"{url}{search_item}")
            if next: next.send(d.page_source)
            
        # options = Options()
        # options.headless = headless
        # driver = webdriver.Firefox(options=options,
        #                         executable_path=r"/home/mint/Desktop/Development/shopping_assistant/gecko/geckodriver")
    
        # driver.get(f"{url}{search_item}")
        # page_source = driver.page_source.deepcopy()
        # driver.quit()
        

    
# @coroutine
def filter_search_result(filter: ColesFilter, next=None):
    print(f"Open for Filtering Products. Filter: {filter}")
    while True:
        page_source: str = (yield)
        soup = BeautifulSoup(page_source, 'html.parser',
                             parse_only=filter())

        if next: next.send(soup)

# @coroutine     
def identify_products(next=None):
    print("Open for Identifying Products")
    product_count = 0
    while True:
        soup: BeautifulSoup = (yield)
        for header in soup.find_all("header", class_="product-header"):
            item = ColesItem(
                full_name=header.find('span', class_="accessibility-inline").text,
                brand=header.find('span', class_="product-brand").text,
                name=header.find('span', class_="product-name").text,
                size=header.find('span', class_="package-size").text,
                dollar=header.find('span', class_="dollar-value").text,
                cent=header.find('span', class_="cent-value").text,
                unit_price=header.find('span', class_="package-price").text,
                id=header.find("h3", class_="product-title")['data-itemid'],
                link=header.find("a", class_="product-image-link")['href'],
                partnumber=header.find("h3", class_="product-title")['data-partnumber']
            )
                    
            if next: next.send(item)
            
def normalize_item(next=None):
    print("Open for Normalisating ColesItems to Dictionary")
    while True:
        item: ColesItem = (yield)
        item_dict = item.to_dict()
        
        normalize_item = {
            "id" : item_dict['id'],
            "full_name": item_dict['full_name'],
            "brand": item_dict['brand'],
            "size": item_dict["size"],
            "link": item_dict['link'],
            "partnumber" : item_dict['partnumber'],
            "price_history": [{
                "date": datetime.datetime.utcnow(),
                "price": item_dict['price'],
                "dollar": item_dict['dollar'],
                "cent": item_dict['cent'],
                "unit_price": item_dict['unit_price'],
                "sale_type": item_dict['sale_type'],
            }]
        }   
        
        if next: next.send(normalize_item)
            
def printer(next=None):
    while True:
        _ = (yield)
        print(_)
        
def save_to_db(next=None):
    client = MongoClient(os.environ.get('HOST'),
                         username=os.environ.get('USERNAME'),
                         password=os.environ.get('PASSWORD'),
                         authSource=os.environ.get('AUTHSOURCE'))
    db = client.test
    collection = db.coles_item_3
    print("Open to database")
    while True:
        item: dict = (yield)
        
        search_query = {"id": item['id']}
        if result := collection.find_one(search_query):
            update = dict()
            update['$set'] = dict()
            if result['full_name'] != item['full_name']:
                update['$set']['full_name'] = item['full_name']
            if result['brand'] != item['brand']:
                update['$set']['brand'] = item['brand']
            if result['size'] != item['size']:
                update['$set']['size'] = item['size']
        
            update["$push"] = {"price_history": item['price_history'][0]}
            _ = collection.update_one(search_query, update).modified_count
        else:
            _ = collection.insert_one(item).inserted_id
            
        if next: next.send(_)
            

def main():
    
    p = printer()
    to_db = save_to_db(next=p)
    normalize = normalize_item(next=to_db)
    identifier = identify_products(next=normalize)
    products = filter_search_result(ColesFilter.AllProducts, next=identifier)
    item_search = coles_item(headless=False, next=products)
    
    
    next(item_search)
    next(products)
    next(identifier)
    next(normalize)
    next(to_db)
    next(p)
        
    while True:
        item = input("What Coles Item are you looking for? ")
        if item: item_search.send(item)
        
            
            
            

if __name__ == "__main__":
    main()
    
    # from pymongo import MongoClient
    # client = MongoClient("local-pi-02",
    #                      username="Test1",
    #                      password="test",
    #                      authSource="test")
    # db = client.test
    # collection = db.movies
    # print(collection.find_one())