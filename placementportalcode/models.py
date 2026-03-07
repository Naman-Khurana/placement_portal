from .extensions import db
from .enums.role import RoleEnum 
from .enums.approval_status import DriveApprovalStatusEnum, CompanyEnumStatus
from .enums.application_status import ApplicationStatusEnum 
from datetime import datetime,date
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False,unique=True)
    password_hash=db.Column(db.String(255),nullable=False)
    name=db.Column(db.String(100),nullable=False)
    dob=db.Column(db.Date)
    role=db.Column(db.String(20),default=RoleEnum.STUDENT.value,nullable=False)
    department=db.Column(db.String(100),nullable=True)
    resume_path = db.Column(db.String(255), nullable=True)  # new column
    eligible = db.Column(
        db.Boolean,
        nullable=True,
        default=True
    )
    applications=db.relationship(
        "Application",
        back_populates='student',
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    company = db.relationship(
        "Company",
        back_populates="user",
        uselist=False,   # one-to-one
        cascade="all, delete-orphan"
    )
    
    


class Company(db.Model):
    __tablename__ = "company"
    company_id=db.Column(db.Integer,primary_key=True)
    company_name=db.Column(db.String(100),nullable=False)
    hr_contact=db.Column(db.String(100),nullable=False)
    company_website=db.Column(db.String(100),nullable=False)
    approval_status=db.Column(db.String(20),
                              default=CompanyEnumStatus.PENDING.value,
                              nullable=False
                              )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        unique=True   # ensures one-to-one
    )
    drives=db.relationship(
        "PlacementDrive",
        back_populates='company',
        cascade="all, delete-orphan"
    )
    user = db.relationship("User", back_populates="company")



class PlacementDrive(db.Model):
    __tablename__ = "placement_drive"
    drive_id=db.Column(db.Integer,primary_key=True)
    drive_name = db.Column(db.String(100), nullable=False)
# to be corrected
    company_id=db.Column(
        db.Integer,
        db.ForeignKey("company.company_id"),
        nullable=False,
    )
    job_title=db.Column(db.String(100),nullable=False)
    job_desc=db.Column(db.String(1000),nullable=False)
    eligibility_criteria=db.Column(db.String(500),nullable=False)
    status=db.Column(db.String(20)
                     ,default=DriveApprovalStatusEnum.PENDING.value
                     ,nullable=False)
    application_deadline=db.Column(db.DateTime,nullable=False)
    ctc = db.Column(
        db.String(50),
        nullable=False,
        default="Not Disclosed"
    )
    company=db.relationship(
        "Company",
        back_populates="drives"
    )

    applications=db.relationship(
        "Application",
        back_populates="drive",
        cascade="all, delete-orphan"
    )






class Application(db.Model):
    __tablename__ = "application"
    application_id=db.Column(db.Integer,primary_key=True)
    application_date=db.Column(db.Date,nullable=False,default=date.today)
    status=db.Column(db.String(20),default=ApplicationStatusEnum.APPLIED.value,nullable=False)

    student_id=db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
    )
    student=db.relationship(
        "User",
        back_populates="applications"
    )

    drive_id=db.Column(
        db.Integer,
        db.ForeignKey("placement_drive.drive_id"),
        nullable=False,
    )
    drive=db.relationship(
        "PlacementDrive",
        back_populates="applications"
    )

    __table_args__=(
        db.UniqueConstraint("student_id","drive_id",name="unique_student_drive"),
    )
