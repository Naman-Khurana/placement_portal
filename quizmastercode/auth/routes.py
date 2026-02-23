from flask import Blueprint,request,session
from quizmastercode.models import User
from http import HTTPMethod
from enums.user import UserEnum 
from enums.role import RoleEnum
from utils.responses import success_response,error_response
from utils.db import save,commit_session


auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/login", methods=[HTTPMethod.POST])
def login():
    data=request.json
    user=User.query.filter_by(username=data[UserEnum.USERNAME.value]).first()

    if not data.get(UserEnum.USERNAME.value) or data.get(UserEnum.PASSWORD.value):
        return error_response("Missing credentials")

    if not user:
        return error_response("User Not Found",404)

    if not user.check_password(data[UserEnum.PASSWORD.value]):
        return error_response("Invalid Password",401)
    
    session["user_id"]=user.id

    return success_response("Login Successful")

@auth_bp.route("/logout" , methods=[HTTPMethod.POST])
def logout():
    session.pop("user_id",None)
    return success_response("Logged out")

@auth_bp.route("/signup", methods=[HTTPMethod.POST])
def signup():
    data=request.json
    
    #missing fields check
    if not data.get(UserEnum.USERNAME.value) or not data.get(UserEnum.PASSWORD.value) or not data.get(UserEnum.NAME.value):
        return error_response("Missing required fields")
    
    #duplicate username check
    if User.query.filter_by(username=data[UserEnum.USERNAME.value]).first():
        return error_response("Username already exists")
    
    user=User(
        username=data[UserEnum.USERNAME.value],
        name=data[UserEnum.NAME.value],
        role=RoleEnum.USER.value
    )

    user.set_password(data[UserEnum.PASSWORD.value])
    #save and commit the user to db
    save(user)
    commit_session()

    return success_response("User created successfully",201)
    
