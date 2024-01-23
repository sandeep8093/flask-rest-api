import json
from bson.objectid import ObjectId
from flask import request
from app.model.db import ConnectDB



class ProductService:
   
    def add_product( data):    
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        products = mongodb_connection.shop["products"]
        print(data)
        products.insert_one(data)
        output = {'Status': 'Successfully Inserted','data':data}
        return output

    def get_product(self):                 
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        products = mongodb_connection.shop["products"]
        print(products)
        documents = products.find()
        return {'products':documents}

    def get_one_product(data):                 
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        products = mongodb_connection.shop["products"]
        objInstance = ObjectId(data['product_id'])
        documents = products.find_one({"_id":objInstance})
        if documents:
            return {'Requested product':documents}   
        else:
            return {'Product not found'}     

    def update_product(product_id,data):          
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        products = mongodb_connection.shop["products"]
        objInstance = ObjectId(product_id)
        response = products.update_one(
            {"_id": objInstance},
            {
                "$set": data
            }
           )
        return {"successfully updated"}
      

    def delete_product(data):          
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        products = mongodb_connection.shop["products"]
        objInstance = ObjectId(data['product_id'])
        response = products.delete_one({"_id": objInstance})
        return {"successfully deleted"}


