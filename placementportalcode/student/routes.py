from flask import Blueprint,Flask,session,url_for,redirect,render_template,request
from http import HTTPMethod
from placementportalcode.models import User,Company,PlacementDrive,Application
from placementportalcode.enums.modelsenum import ApplicationEnum 
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.approval_status import CompanyEnumStatus,DriveApprovalStatusEnum
from placementportalcode.enums.application_status import ApplicationStatusEnum
from datetime import datetime ,date
from placementportalcode.extensions import db
import os
from flask import current_app
from werkzeug.utils import secure_filename


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
    student_applications=Application.query.filter(Application.student_id==user.id).all()
    return render_template("student/dashboard.html",registered_companies=registered_companies,student=user,student_applications=student_applications)
    

@student_bp.route('/<int:student_id>/<int:company_id>/drives',methods=[HTTPMethod.GET])
def company_drives(student_id,company_id):
    company = Company.query.get(company_id)

    if not company:
        return redirect(url_for('student.dashboard'))
    now= datetime.now()
    current_drives=PlacementDrive.query.filter(PlacementDrive.company_id==company_id,PlacementDrive.status==DriveApprovalStatusEnum.APPROVED.value, PlacementDrive.application_deadline>=now)
    rejected_applications=Application.query.filter(Application.student_id==student_id,Application.status=='rejected')
    shortlistedOrHired_applications=Application.query.filter(Application.student_id==student_id,Application.status.in_(["shortlisted", "hired"]))
    applications = Application.query.filter(Application.student_id==student_id,Application.status=='applied')
    student=User.query.get(student_id)
    rejected_application_ids={app.drive_id for app in rejected_applications}
    applied_drive_ids= {app.drive_id for app in applications}
    shortlistedOrHired_application_ids={app.drive_id for app in shortlistedOrHired_applications}
    return render_template('student/company-details.html',company=company,current_drives=current_drives,student=student,applied_drive_ids=applied_drive_ids,rejected_application_ids=rejected_application_ids,shortlistedOrHired_application_ids=shortlistedOrHired_application_ids)

@student_bp.route('/<int:student_id>/<int:drive_id>/application', methods=[HTTPMethod.POST])
def apply_drive(student_id,drive_id):
   
    student_id = request.form.get("student_id")
    drive_id = request.form.get("drive_id")
    company_id=request.form.get('company_id')

    drive = PlacementDrive.query.get_or_404(drive_id)
    student = User.query.get_or_404(student_id)
    company=Company.query.get_or_404(company_id)
    
    checkApplication=Application.query.filter(Application.student_id==student_id , Application.drive_id==drive_id).first()
    if checkApplication:
        return redirect(url_for('student.dashboard'))
    
    application=Application(
        application_date=date.today(),
        status=ApplicationStatusEnum.APPLIED.value,
        student_id=student_id,
        drive_id=drive_id
    )

    db.session.add(application)
    db.session.commit()

    if not company :
        return redirect(url_for('student.dashboard'))
    return redirect(url_for('student.company_drives', company_id=company.company_id,student_id=student_id))

@student_bp.route("/withdraw_application", methods=[HTTPMethod.POST])
def withdraw_application():

    student_id = session.get("user_id")
    drive_id = request.form.get("drive_id")

    if not student_id or not drive_id:
        return redirect(url_for("student.dashboard"))

    application = Application.query.filter(
        Application.student_id == student_id,
        Application.drive_id == drive_id
    ).first()

    if application:
        db.session.delete(application)
        db.session.commit()

    return redirect(request.referrer)    


@student_bp.route('/edit-profile',methods=[HTTPMethod.POST])
def edit_profile():
    user_id = session.get("user_id")
    student = User.query.get_or_404(user_id)

    student.name = request.form.get("name")
    student.department = request.form.get("department")

    dob = request.form.get("dob")
    if dob:
        student.dob = datetime.strptime(dob, "%Y-%m-%d").date()

    file = request.files.get("resume")

    if file and file.filename != "":
        filename = secure_filename(file.filename)

        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        student.resume_path = f"uploads/resumes/{filename}"


        student.resume_path = f"uploads/resumes/{filename}"
    db.session.commit()
    
    return redirect(url_for("student.dashboard"))
