from flask import Blueprint,render_template,session,redirect,url_for,abort
from http import HTTPMethod 
from flask import request
from placementportalcode.models import User,Company,PlacementDrive,Application
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.modelsenum import UserEnum
from placementportalcode.enums.approval_status import CompanyEnumStatus,DriveApprovalStatusEnum
from placementportalcode.enums.application_status import ApplicationStatusEnum
from placementportalcode.extensions import db
from datetime import datetime
from sqlalchemy import or_
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
    blacklisted_companies=Company.query.filter_by(approval_status=CompanyEnumStatus.BLACKLISTED.value)
    registered_students=User.query.filter_by(role=RoleEnum.STUDENT.value )
    requested_drives=PlacementDrive.query.filter(PlacementDrive.status==DriveApprovalStatusEnum.PENDING.value)
    rejected_drives=PlacementDrive.query.filter(PlacementDrive.status==DriveApprovalStatusEnum.REJECT.value)

    ongoing_drives=PlacementDrive.query.filter(PlacementDrive.status=='approved',PlacementDrive.status==DriveApprovalStatusEnum.APPROVED.value)
    student_applications=Application.query.all()

   
    return render_template("admin/dashboard.html",company_applications=company_applications,registered_companies=registered_companies,registered_students=registered_students,ongoing_drives=ongoing_drives,requested_drives=requested_drives,student_applications=student_applications,blacklisted_companies=blacklisted_companies,rejected_drives=rejected_drives)

    
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


@admin_bp.route("/drive/<int:drive_id>/update_status",methods=[HTTPMethod.POST])
def update_drive_status(drive_id):
    drive=PlacementDrive.query.get_or_404(drive_id)
    action=request.form.get('action')
    
    if(action=='approve'):
        drive.status=DriveApprovalStatusEnum.APPROVED.value
    
    elif action=='reject':
        drive.status=DriveApprovalStatusEnum.REJECT.value
    elif action=='close':
        drive.status=DriveApprovalStatusEnum.CLOSED.value
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


@admin_bp.route("/application/update_status",methods=[HTTPMethod.POST])
def update_application_status():
    application=Application.query.get_or_404('application_id')
    action=request.form.get('action')
    
    
    if(action=='shortlisted'):
        application.status=ApplicationStatusEnum.SHORTLISTED.value
    elif action=='rejected':
        application.status=ApplicationStatusEnum.REJECTED.value
    elif action=='selected':
        application.status=ApplicationStatusEnum.SELECTED.value
    elif action=='hired':
        application.status=ApplicationStatusEnum.HIRED.value
    elif action=='waitlisted':
        application.status=ApplicationStatusEnum.WAITLISTED.value
    else:
        abort(400)

    db.session.commit()
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/search", methods=["GET"])
def search():

    query = request.args.get("query", "").strip()

    students = []
    companies = []

    if query:
        students = User.query.filter(
            User.role == RoleEnum.STUDENT.value,
            or_(
                User.name.ilike(f"%{query}%"),
                User.username.ilike(f"%{query}%")
            )
        ).all()

        companies = Company.query.filter(
            Company.company_name.ilike(f"%{query}%")
        ).all()

    return render_template(
        "admin/search_results.html",
        query=query,
        search_students=students,
        search_companies=companies
    )
    
    
