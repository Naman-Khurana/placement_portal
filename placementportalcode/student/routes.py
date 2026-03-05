from flask import Blueprint,Flask,session,url_for,redirect,render_template,request
from http import HTTPMethod
from placementportalcode.models import User,Company,PlacementDrive
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.approval_status import CompanyEnumStatus,DriveApprovalStatusEnum
from datetime import datetime


student_bp=Blueprint("student",__name__,url_prefix="/student")

@student_bp.route("/dashboard",methods=[HTTPMethod.GET])
def dashboard():
    user_id=session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.STUDENT.value:
        return redirect(url_for("auth.login"))
    
    registered_companies=Company.query.filter_by(approval_status=CompanyEnumStatus.APPROVED.value)
   
    return render_template("student/dashboard.html",registered_companies=registered_companies)
    

@student_bp.route('/company/<int:company_id>/drives',methods=[HTTPMethod.GET])
def company_drives(company_id):
    company = Company.query.get(company_id)

    if not company:
        return redirect(url_for('student.dashboard'))
    now= datetime.now()
    current_drives=PlacementDrive.query.filter(PlacementDrive.status!=DriveApprovalStatusEnum.CLOSED.value, PlacementDrive.application_deadline>=now)
    
    return render_template('student/company-details.html',company=company,current_drives=current_drives)

