from flask import Flask ,Blueprint,session,render_template,redirect,url_for,request
from placementportalcode.models import Company,User,PlacementDrive
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.modelsenum import PlacementDriveEnum,UserEnum,CompanyEnum
from http import HTTPMethod
from placementportalcode.extensions import db
from datetime import datetime,date

company_bp=Blueprint("company",__name__,url_prefix="/company")

@company_bp.route("/dashboard",methods=[HTTPMethod.GET] )
def dashboard():
    user_id=session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))
    user=User.query.get(user_id)
    if not user or user.role!=RoleEnum.COMPANY  .value:
        return redirect(url_for("auth.login"))
    
    
    

    current_company=user.company
    now=datetime.now()


    upcoming_drives=PlacementDrive.query.filter(
        PlacementDrive.company_id==current_company.company_id,
        PlacementDrive.application_deadline >=now
    ).order_by(PlacementDrive.application_deadline.asc()).all()\
    
    closed_drives=PlacementDrive.query.filter(
        PlacementDrive.company_id==current_company.company_id,
        PlacementDrive.application_deadline < now
    ).order_by(PlacementDrive.application_deadline.asc()).all()

    return render_template("company/dashboard.html",upcoming_drives=upcoming_drives, closed_drives=closed_drives)

@company_bp.route("/create-drive",methods=[HTTPMethod.POST])
def create_drive():

    drive_name=request.form.get(PlacementDriveEnum.DRIVE_NAME.value)
    job_title=request.form.get(PlacementDriveEnum.JOB_TITLE.value)
    job_desc=request.form.get(PlacementDriveEnum.JOB_DESC.value)
    eligibility_criteria=request.form.get(PlacementDriveEnum.ELIGIBILITY_CRITERIA.value)
    deadline_raw = request.form.get(PlacementDriveEnum.APPLICATION_DEADLINE.value)

    application_deadline = datetime.strptime(
        deadline_raw, "%Y-%m-%dT%H:%M"
    )
    user_id=session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))
    
    user= User.query.get(user_id)

    if not user or user.role!=RoleEnum.COMPANY.value:
        return redirect(url_for("auth.login"))
    
    company=user.company
    if not company:
        return redirect(url_for("auth.login"))
    
    company_id=company.company_id

    new_drive=PlacementDrive(
        drive_name=drive_name,
        company_id=company_id,
        job_title=job_title,
        job_desc=job_desc,
        eligibility_criteria=eligibility_criteria,
        application_deadline=application_deadline

    )

    db.session.add(new_drive)
    db.session.commit()

    return redirect(url_for("company.dashboard"))
    