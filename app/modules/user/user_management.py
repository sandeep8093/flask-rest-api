import string
import random
import jwt
from app.model.db import ConnectDB


class UserService:

    def __init__(self, email='', password='',user_role='',jwt_token='token'):
        self.email = email
        self.password = password
        self.user_role=user_role
        self.jwt_token=jwt_token

    def register(self,data):
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        users = mongodb_connection.shop["users"]
        print(data)
        if data["email"]!=None and data["password"]!=None and data["user_role"]!=None:
            already_registered=users.find_one({"email":data['email']})
            if already_registered:
                return {'already registered with this mail '}
            else:  
                data['jwt_token']=' '  
                users.insert_one(data)
                return {'Status': 'Successfully Registered','data':data}
        else:
            return {"Please fill the required fields for user"}
       

    def login(self, data):
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        users = mongodb_connection.shop["users"]
        email = data["email"]
        password =data["password"]
        my_secret='hello world'
        
        registered_user=users.find_one({"email":email})
        if registered_user==None:
            return {"email is not registered"}
        else:
            if password!=registered_user['password']:
                return {"wrong password"}
            else:
                payload={
                    "password":registered_user['password'],
                    "email":registered_user['email'],
                    "user_role":registered_user['user_role']
                }
                
                token = jwt.encode(
                    payload,
                    my_secret, algorithm="HS256"
                )
                newvalues = { "$set": { "jwt_token":token } }
                users.update_one(registered_user, newvalues)
                print(token)
                return {"status": "success", "data": payload ,"token":token}
    
    def get_user(self,data):
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        users = mongodb_connection.shop["users"]
        if data!=None:
            req_user=users.find_one({"email":data})
            return req_user
        else:
            return {"Please give the correct id for user"}  

    def logout(current_user):
        connection = ConnectDB()
        mongodb_connection = connection.connect_db()
        users = mongodb_connection.shop["users"]
        newvalues = { "$set": { "jwt_token":'' } }
        users.update_one(current_user, newvalues)
        return {"status":"Successfully logged out","user":current_user}
