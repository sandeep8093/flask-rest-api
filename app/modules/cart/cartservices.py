import json
from bson.objectid import ObjectId
from flask import request
from app.model.db import ConnectDB



class CartService:
    def add_cart(data,user_id):    
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        cart = mongodb_connection.shop["cart"]
        products = mongodb_connection.shop["products"]
        users = mongodb_connection.shop["users"]
        req_user=users.find_one({"_id":ObjectId(user_id)})
        if req_user:
            objInstance = ObjectId(data['product_id'])
            req_product = products.find_one({"_id":objInstance})
            data["user_id"]=ObjectId(user_id)
            if req_product:
                if req_product["available_copies"] >= data["quantity"]:
                    print(req_product)
                    #req_product["available_copies"]=req_product["available_copies"]-data["quantity"]
                    quantity=req_product["available_copies"]-data["quantity"]
                    newvalues = { "$set": { "available_copies": quantity } }
                    products.update_one(req_product, newvalues)
                    print(req_product)
                    cart.insert_one(data)
                    output = {'Status': 'Successfully Inserted into cart','data':data}
                    return output
                else:
                    return{"insufficient quantity"}    
            else:
                return {"this product is not available"} 
        else:
            return {"user not available"}

    def update_cart(cart_id,data,user_id):
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        cart = mongodb_connection.shop["cart"]
        products = mongodb_connection.shop["products"]
        users = mongodb_connection.shop["users"]
        req_user=users.find_one({"_id":ObjectId(user_id)})
        if req_user:
            required_cart=cart.find({"_id":ObjectId(cart_id),"user_id":ObjectId(user_id)})
            if required_cart:
                for item in required_cart:
                    req_product=products.find_one({"_id":ObjectId(item['product_id'])})
                    if req_product:  
                        if req_product['available_copies']+item['quantity']-data['quantity']>=0:
                            new_quantity=req_product['available_copies']+item['quantity']-data['quantity']
                            newvalues = { "$set": { "available_copies":new_quantity } }
                            products.update_one(req_product, newvalues)
                            newvalues1 = { "$set": { "quantity": data['quantity'] } }
                            cart.update_one(item, newvalues1)
                        else:
                            return {"insufficient quantity"}       
                    else:
                        return {"product does not exists"}
                return {"updated succesfully"}                
            else:
                return {"this cart does not exists or unauthorised user "}    
        else:
            return {"user not available"}

    def delete_cart(user_id):          
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        cart = mongodb_connection.shop["cart"]
        products=mongodb_connection.shop["products"]
        required_cart=cart.find({"user_id":ObjectId(user_id)})
        if required_cart:
            for item in required_cart:
                print(item)
                req_product=products.find_one({"_id":ObjectId(item['product_id'])})
                if req_product:
                    new_quantity=item['quantity']+req_product['quantity']
                    newvalues = { "$set": { "available_copies":new_quantity } }
                    products.update_one(req_product, newvalues)
                else:
                    return {"Product not found"}    
                print(item['_id'])  
                cart.delete_one({"_id": ObjectId(item['_id'])})
            return {"successfully deleted"}    
        else:
            return{"cart not found"}

    def remove_one_from_cart(data,user_id):
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        cart = mongodb_connection.shop["cart"]
        products=mongodb_connection.shop["products"]
        required_cart=cart.find_one({"product_id":data['product_id'],"user_id":ObjectId(user_id)})
        print(required_cart)
        if required_cart:
            req_product=products.find_one({"_id":ObjectId(data['product_id'])})
            if req_product:
                new_quantity=required_cart['quantity']+req_product['available_copies']
                newvalues = { "$set": { "available_copies":new_quantity } }
                products.update_one(req_product, newvalues)
            else:
                return {"Product not found"}    
            return {"successfully removed this product"}    
        else:
            return{"cart not found"}


    def get_cart(self,user_id):                 
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        cart = mongodb_connection.shop["cart"]
        req_data = cart.find({"user_id":ObjectId(user_id)})
        return {'cart':req_data}        

                      

        