

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
    
    
# @coroutine
def filter_search_result(filter: ColesFilter, target):
    print("Accepting Search Results")
    while True:
        page_source: str = (yield)
        soup = BeautifulSoup(page_source, 'html.parser',
                             parse_only=filter())
        target.send(soup)

# @coroutine     
def identify_products():
    print("Open for finding products")
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
            
            print(item)
            product_count += 1
            print(product_count)

def main():
    # get_milk()
    
    printer = identify_products()
    
    everyday = filter_search_result(ColesFilter.New, printer)
    
    next(printer)
    next(everyday)
    
    with open("stores/coles/milk.html", "r") as milk_page:
        everyday.send(milk_page)
        

            
            
            
            
        
        
        
        
        
        
        
        
        
    

if __name__ == "__main__":
    main()