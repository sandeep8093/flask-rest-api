from bson import json_util
from flask import request, Response

from app import app
from app.middleware.auth_middleware import token_required
from app.modules.product.productservice import ProductService
from app.modules.user.user_management import UserService
from app.modules.cart.cartservices import CartService

@app.route('/', methods=['GET'])
def hello():
    return 'Hello world'
#Authentication Services

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if data is None or data == {}:
        return Response(response=json_util.dumps({"Error": "Please provide  information"}),
                        status=400, mimetype='application/json')
    response = UserService().register(data)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data is None or data == {}:
        return Response(response=json_util.dumps({"Error": "Please provide  information"}),
                        status=400, mimetype='application/json')
    response = UserService().login(data)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


@app.route('/get_user', methods=['POST'])
@token_required
def get_user(current_user):
    return Response(response=json_util.dumps(current_user), status=200,
                    mimetype='application/json')

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    response=UserService.logout(current_user)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')




#Product Services

#all user types have access
@app.route('/get_product', methods=['GET'])
@token_required
def get_product(self):
    response = ProductService().get_product()
    print(response)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


#all user types have access
@app.route('/get_one_product', methods=['GET'])  # Read MongoDB Document, through API and METHOD - GET
@token_required
def get_one_product(data):
    data = request.json
    if data is None or data == {}:
        return Response(response=json_util.dumps({"Error": "Please provide connection information"}),
                        status=400, mimetype='application/json')
    response = ProductService.get_one_product(data)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


#only admin has access
@app.route('/add_product', methods=['POST'])  # Create MongoDB Document, through API and METHOD - POST
@token_required
def add_product(current_user):
    data = request.json
    print(current_user)
    if current_user['user_role']=='admin':
        response = ProductService.add_product(data)
        return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')
    else:
        return {"You are not allowed to do that"}
  
#only admin has access
@app.route('/update_product/<product_id>', methods=['POST']) 
@token_required    
def update_product(current_user,product_id):
    data = request.json
    if current_user['user_role']=='admin':
        response = ProductService.update_product(product_id,data)
        return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')
    else:
        return {"You are not allowed to do that"}                

#only admin has access
@app.route('/delete_product', methods=['POST']) 
@token_required    
def delete_product(current_user):
    data = request.json
    if current_user['user_role']=='admin':
        response = ProductService.delete_product(data)
        return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')
    else:
        return {"You are not allowed to do that"}                


#Cart Services

@app.route('/add_cart', methods=['POST'])  # Create MongoDB Document, through API and METHOD - POST
@token_required
def add_cart(current_user):
    data = request.json
    print(current_user)
    response = CartService.add_cart(data,current_user['_id'])
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')
   

@app.route('/update_cart/<cart_id>', methods=['POST']) 
@token_required    
def update_cart(current_user,cart_id):
    data = request.json
    response = CartService.update_cart(cart_id,data,current_user['_id'])
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')

@app.route('/delete_cart', methods=['POST']) 
@token_required    
def delete_cart(current_user):
    response = CartService.delete_cart(current_user['_id'])
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')

@app.route('/remove_one_from_cart', methods=['POST']) 
@token_required    
def remove_one_from_cart(current_user):
    data = request.json
    response = CartService.remove_one_from_cart(data,current_user['_id'])
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


@app.route('/get_cart', methods=['GET'])
@token_required
def get_cart(current_user):
    response = CartService().get_cart(current_user['_id'])
    print(response)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')                    
        