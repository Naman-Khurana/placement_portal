from flask import Blueprint,Flask,session,url_for,redirect,render_template,request
from http import HTTPMethod
from placementportalcode.models import User,Company
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.approval_status import CompanyEnumStatus

student_bp=Blueprint("student",__name__,url_prefix="/student")

@student_bp.route("/dashboard",methods=[HTTPMethod.GET])
def dashboard():
    user_id=session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.STUDENT.value:
        return redirect(url_for("auth.login"))
    
    registered_organizations=Company.query.filter_by(approval_status=CompanyEnumStatus.APPROVED.value)
   
    return render_template("student/dashboard.html",registered_organizations=registered_organizations)
    