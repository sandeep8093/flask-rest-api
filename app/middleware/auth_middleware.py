from functools import wraps
import jwt
from flask import request, abort
from flask import app
from app.modules.user.user_management import UserService

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, 'hello world', algorithms="HS256")
            current_user=UserService().get_user(data["email"])
           
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if current_user['jwt_token']=='':
                return {
                "message": "logged out Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            
            
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated