from flask import Blueprint,render_template,session,redirect,url_for,abort
from http import HTTPMethod 
from flask import request
from placementportalcode.models import User,Company,PlacementDrive
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.modelsenum import UserEnum
from placementportalcode.enums.approval_status import CompanyEnumStatus,DriveApprovalStatusEnum
from placementportalcode.extensions import db
from datetime import datetime
admin_bp=Blueprint("admin",__name__,url_prefix="/admin")

@admin_bp.route("/dashboard",methods=[HTTPMethod.GET] )
def dashboard():
    user_id=session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))
    user=User.query.get(user_id)
    if not user:
        return redirect(url_for("auth.login"))
    if user.role!=RoleEnum.ADMIN.value:
        return redirect(url_for("auth.login"))
    now=datetime.now()
    company_applications=Company.query.filter_by(approval_status=CompanyEnumStatus.PENDING.value)
    registered_companies=Company.query.filter_by(approval_status=CompanyEnumStatus.APPROVED.value)
    registered_students=User.query.filter_by(role=RoleEnum.STUDENT.value )
    ongoing_drives=PlacementDrive.query.filter(PlacementDrive.application_deadline <now,PlacementDrive.status!=DriveApprovalStatusEnum.CLOSED.value)
    return render_template("admin/dashboard.html",company_applications=company_applications,registered_companies=registered_companies,registered_students=registered_students,ongoing_drives=ongoing_drives)
    
@admin_bp.route("/company/<int:company_id>/update_status",methods=[HTTPMethod.POST])
def update_company_status(company_id):
    company=Company.query.get_or_404(company_id)
    action=request.form.get('action')
    
    if(action=='approve'):
        company.approval_status=CompanyEnumStatus.APPROVED.value
    
    elif action=='blacklist':
        company.approval_status=CompanyEnumStatus.BLACKLISTED.value
    else:
        abort(400)

    db.session.commit()
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/student/<int:student_id>/update_status",methods=[HTTPMethod.POST])
def update_student_status(student_id):
    student=User.query.get_or_404(student_id)
    action=request.form.get('action')
    
    if(action=='whitelist'):
        student.eligible=True
    
    elif action=='blacklist':
        student.eligible=False
    else:
        abort(400)

    db.session.commit()
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/drive/<int:drive_id>/update_status",methods=[HTTPMethod.POST])
def update_drive_status(drive_id):
    drive=PlacementDrive.query.get_or_404(drive_id)
    action=request.form.get('action')
    
    if(action=='close'):
        drive.status=DriveApprovalStatusEnum.CLOSED.value
    
    elif action=='approve':
        drive.status=DriveApprovalStatusEnum.APPROVED.value
    else:
        abort(400)

    db.session.commit()
    return redirect(url_for("admin.dashboard"))