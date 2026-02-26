from flask import Blueprint,request,session, render_template, request, redirect, url_for, session, flash
from placementportalcode.models import User
from http import HTTPMethod
from placementportalcode.enums.modelsenum import UserEnum 
from placementportalcode.enums.role import RoleEnum

from placementportalcode.utils.responses import success_response,error_response
from placementportalcode.utils.db import save,commit_session


auth_bp=Blueprint("auth",__name__)

@auth_bp.route("/login", methods=['GET','POST'])
def login():
    if(request.method=='GET'):
        return render_template("auth/login.html")
    
    #POST LOGIC
    data=request    

    username=data.form.get(UserEnum.USERNAME.value)
    password=data.form.get(UserEnum.PASSWORD.value)

    

    if not username or not password:
        flash("Missing credentials")
        return redirect(url_for("auth.login"))
    
        
    user=User.query.filter_by(username=username).first()

    if not user:
        flash("User Not Found")
        return redirect(url_for("auth.login"))

    if not user.check_password(password):
        flash("Invalid password")
        return redirect(url_for("auth.login"))
    
    
    
    session["user_id"]=user.id
    print(user.role)
    if user.role == RoleEnum.ADMIN.value:
        return redirect(url_for("admin.dashboard"))
    return success_response("Login Successful")

@auth_bp.route("/logout" , methods=[HTTPMethod.GET,HTTPMethod.POST])
def logout():
    session.pop("user_id",None)
    return success_response("Logged out")

@auth_bp.route("/signup", methods=[HTTPMethod.GET,HTTPMethod.POST])
def signup():
    if(request.method==HTTPMethod.GET):
        return render_template("auth/signup.html")
    data=request


    username=data.form.get(UserEnum.USERNAME.value)
    password=data.form.get(UserEnum.PASSWORD.value)
    name=data.form.get(UserEnum.NAME.value)

    

    
    
    #missing fields check
    if not username or not password or not name:
        flash("missing credentials")
        return redirect(url_for("auth.signup")) 
    
    #duplicate username check
    if User.query.filter_by(username).first():
        flash("Username already exists")
        return redirect(url_for("auth.signup")) 
       
    user=User(
        username=username,
        name=name,
        role=RoleEnum.STUDENT.value
    )

    user.set_password(password)
    #save and commit the user to db
    save(user)
    commit_session()

    return success_response("User created successfully",201)
    
