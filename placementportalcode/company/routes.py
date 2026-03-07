from flask import Flask ,Blueprint,session,render_template,redirect,url_for,request
from placementportalcode.models import Company,User,PlacementDrive,Application
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.modelsenum import PlacementDriveEnum,UserEnum,CompanyEnum
from http import HTTPMethod
from placementportalcode.extensions import db
from datetime import datetime,date
from placementportalcode.enums.approval_status import DriveApprovalStatusEnum
from sqlalchemy import or_

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
        PlacementDrive.application_deadline >=now,
        PlacementDrive.status!=DriveApprovalStatusEnum.CLOSED.value
    ).order_by(PlacementDrive.application_deadline.asc()).all()\
    
    closed_drives=PlacementDrive.query.filter(
        PlacementDrive.company_id==current_company.company_id,
        or_(
            PlacementDrive.application_deadline < now,
            PlacementDrive.status==DriveApprovalStatusEnum.CLOSED.value
        )
       
    ).order_by(PlacementDrive.application_deadline.asc()).all()

    return render_template("company/dashboard.html",upcoming_drives=upcoming_drives, closed_drives=closed_drives,current_company=current_company)

@company_bp.route("/create-drive",methods=[HTTPMethod.POST])
def create_drive():

    drive_name=request.form.get(PlacementDriveEnum.DRIVE_NAME.value)
    job_title=request.form.get(PlacementDriveEnum.JOB_TITLE.value)
    job_desc=request.form.get(PlacementDriveEnum.JOB_DESC.value)
    eligibility_criteria=request.form.get(PlacementDriveEnum.ELIGIBILITY_CRITERIA.value)
    deadline_raw = request.form.get(PlacementDriveEnum.APPLICATION_DEADLINE.value)
    ctc=request.form.get(PlacementDriveEnum.CTC.value)
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
        application_deadline=application_deadline,
        ctc=ctc

    )

    db.session.add(new_drive)
    db.session.commit()

    return redirect(url_for("company.dashboard"))
    

@company_bp.route("/update-applicant-status", methods=[HTTPMethod.POST])
def update_applicant_status():

    application_id = request.form.get("application_id")
    status = request.form.get("status")

    application = Application.query.get_or_404(application_id)

    application.status = status

    db.session.commit()

    return redirect(request.referrer)


@company_bp.route("/close-drive", methods=[HTTPMethod.POST])
def close_drive():
    drive_id=request.form.get('drive_id')
    drive=PlacementDrive.query.get_or_404(drive_id)

    drive.status=DriveApprovalStatusEnum.CLOSED.value

    db.session.commit()

    return redirect(request.referrer)


@company_bp.route("/update-drive/<int:id>", methods=["POST"])
def update_drive(id):

    drive = PlacementDrive.query.get_or_404(id)

    deadline = request.form.get("application_deadline")
    ctc = request.form.get("ctc")
    status = request.form.get("status")

    if deadline:
        drive.application_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()

    if ctc:
        drive.ctc = ctc

    if status:
        drive.status = status

    db.session.commit()

    return redirect(url_for("company.dashboard"))

@company_bp.route("/edit-profile", methods=["POST"])
def edit_profile():

    company_id=request.form.get('company_id')
    if not company_id:
        return redirect(url_for("company.dashboard"))
    
    company=Company.query.get_or_404(company_id)
    

    hr_contact = request.form.get("hr_contact")
    company_website = request.form.get("company_website")
    company_name = request.form.get("company_name")

    if hr_contact:
        company.hr_contact=hr_contact
    if company_website:
        company.company_website=company_website
    if company_name:
        company.company_name=company_name
   

    db.session.commit()

    return redirect(url_for("company.dashboard"))