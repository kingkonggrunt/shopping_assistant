

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


from bs4 import BeautifulSoup, SoupStrainer

from coles import ColesItem
from filters import ColesFilter

def get_milk():
    url = "https://shop.coles.com.au/a/national/everything/search/milk"

    options = Options()
    # options.headless = True
    driver = webdriver.Firefox(options=options,
                               executable_path=r"/home/mint/Desktop/Development/shopping_assistant/gecko/geckodriver")
    driver.get(url)
    
    with open('stores/coles/milk.html', 'w') as f:
        f.write(driver.page_source)

    driver.quit()
    
    
# def coroutine(func):
#     def start(*args,**kwargs):
#         cr = func(*args,**kwargs)
#         cr.next()
#         return cr
#     return start
    
    
def coles_item(next=None):
    url = "https://shop.coles.com.au/a/national/everything/search/"
    print("Open to Searching for Products")
    while True:
        search_item = (yield)
        
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options,
                                executable_path=r"/home/mint/Desktop/Development/shopping_assistant/gecko/geckodriver")
    
        driver.get(f"{url}{search_item}")

        if next: next.send(driver.page_source)

        driver.quit()
    
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
            
def printer(next=None):
    while True:
        _ = (yield)
        print(_)

def main():
    # get_milk()
    
    p = printer()
    identifier = identify_products(next=p)
    everyday = filter_search_result(ColesFilter.AllProducts, next=identifier)
    item_search = coles_item(next=everyday)
    
    
    next(item_search)
    next(identifier)
    next(everyday)
    next(p)
    
    # with open("stores/coles/milk.html", "r") as milk_page:
    #     everyday.send(milk_page)
        
    while True:
        item = input("What Coles Item are you looking for? ")
        if item: item_search.send(item)
        
            
            
            

if __name__ == "__main__":
    main()