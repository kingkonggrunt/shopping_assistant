import datetime
from json import load
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()



item_dict = {
    "full_name" : "Abbott's Bakery Gluten Free Farmhouse Wholemeal Bread 500g ",
    "brand" : "Abbott's",
    "name" : "Bakery Gluten Free Farmhouse Wholemeal Bread",
    "size" : "500g ",
    "sale_type" : 0,
    "price" : 7.3,
    "unit_price" : "$1.46 per 100G",
    "dollar" : "7",
    "cent" : ".30",
    "link" : "/a/national/product/abbotts-village-bakery-gluten-fre-wholemeal",
    "partnumber" : "3751790P",
    "id" : "001200549" 
}


new_dict = {
    "id" : item_dict['id'],
    "full_name": item_dict['full_name'],
    "brand": item_dict['brand'],
    "size": item_dict["size"],
    "link": item_dict['link'],
    "partnumber" : item_dict['partnumber'],
    # "sale_type" : item_dict['sale_type'],
    "prices": {
        "date": datetime.datetime.utcnow(),
        "price": item_dict['price'],
        "dollar": item_dict['dollar'],
        "cent": item_dict['cent'],
        "unit_price": item_dict['unit_price']
    }
}

def convert_dictionary(item_dict):
    return {
        "id" : item_dict['id'],
        "full_name": item_dict['full_name'],
        "brand": item_dict['brand'],
        "size": item_dict["size"],
        "link": item_dict['link'],
        "partnumber" : item_dict['partnumber'],
        # "sale_type" : item_dict['sale_type'],
        "prices": [{
            "date": datetime.datetime.utcnow(),
            "price": item_dict['price'],
            "dollar": item_dict['dollar'],
            "cent": item_dict['cent'],
            "unit_price": item_dict['unit_price'],
            "sale_type": item_dict['sale_type'],
        }]
    }
    
    
def send_to_db(new_dict):
    client = MongoClient(os.environ.get('HOST'),
                        username=os.environ.get('USERNAME'),
                        password=os.environ.get('PASSWORD'),
                        authSource=os.environ.get('AUTHSOURCE'))
    db = client.test
    collection = db.coles_item_2   
    
    search_query = {"id": new_dict['id']}
    if result := collection.find_one(search_query):
        update = dict()
        update['$set'] = dict()
        if result['full_name'] != new_dict['full_name']:
            update['$set']['full_name'] = new_dict['full_name']
        if result['brand'] != new_dict['brand']:
            update['$set']['brand'] = new_dict['brand']
        if result['size'] != new_dict['size']:
            update['$set']['size'] = new_dict['size']
        
        update["$push"] = {"prices": new_dict['prices'][0]}
        return collection.update_one(search_query, update)
    else:
        return collection.insert_one(new_dict).inserted_id
        


c_dict = convert_dictionary(item_dict)
send_to_db(c_dict)
