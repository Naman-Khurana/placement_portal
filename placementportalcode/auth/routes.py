from flask import Blueprint,request,session, render_template, request, redirect, url_for, session, flash
from placementportalcode.models import User,Company
from http import HTTPMethod
from placementportalcode.enums.approval_status import CompanyEnumStatus
from placementportalcode.enums.modelsenum import UserEnum ,CompanyEnum
from placementportalcode.enums.role import RoleEnum
from placementportalcode.extensions import db
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
    if user.role==RoleEnum.COMPANY.value:
        return redirect(url_for("company.dashboard"))
    flash(user.role)
    return redirect(url_for("student.dashboard"))

@auth_bp.route("/logout" , methods=[HTTPMethod.GET,HTTPMethod.POST])
def logout():
    session.pop("user_id",None)
    return redirect(url_for("auth.login"))

@auth_bp.route("/company-register" ,methods=['GET','POST'])
def register_company():
    if(request.method=='GET'):
        return render_template("company/register.html")
    data=request
    hr_contact=data.form.get(CompanyEnum.HR_CONTACT.value)
    company_name = data.form.get(CompanyEnum.COMPANY_NAME.value)
    password = data.form.get(UserEnum.PASSWORD.value)
    website = data.form.get(CompanyEnum.COMPANY_WEBSITE.value)


    existing_user = User.query.filter_by(username=hr_contact).first()

    if existing_user: 
        flash("Email already registered.", "danger")
        return redirect(url_for("auth.register_company"))
    

    try:

        user=User(
            username=hr_contact,
            name=company_name,
            role=RoleEnum.COMPANY.value        
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.flush() 

        
        
        company = Company(
                    company_name=company_name,
                    hr_contact=hr_contact,
                    company_website=website,
                    approval_status=CompanyEnumStatus.PENDING.value,
                    user_id=user.id

                )

        db.session.add(company)
        db.session.commit()

        flash("Registration successful. Await admin approval.", "success")
        return redirect(url_for("auth.login"))
    except Exception as e:
        db.session.rollback()
        flash("Something went wrong. Try again.", "danger")
        return redirect(url_for("auth.register_company"))
        

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
    if User.query.filter_by(username=username).first():
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

    return redirect(url_for("auth.login"))
    
