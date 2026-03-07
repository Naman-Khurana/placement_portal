import enum

class UserEnum(str,enum.Enum):
    ID = "id"
    USERNAME = "username"
    PASSWORD="password"
    PASSWORD_HASH = "password_hash"
    NAME = "name"
    QUALIFICATION = "qualification"
    DOB = "dob"
    ROLE = "role"

class CompanyEnum(str, enum.Enum):
    COMPANY_ID = "company_id"
    COMPANY_NAME = "company_name"
    HR_CONTACT = "hr_contact"
    COMPANY_WEBSITE = "company_website"
    APPROVAL_STATUS = "approval_status"

class PlacementDriveEnum(str, enum.Enum):
    DRIVE_ID = "drive_id"
    COMPANY_ID = "company_id"
    JOB_TITLE = "job_title"
    JOB_DESC = "job_desc"
    ELIGIBILITY_CRITERIA = "eligibility_criteria"
    STATUS = "status"
    APPLICATION_DEADLINE = "application_deadline"
    DRIVE_NAME="drive_name"
    CTC="ctc"

class ApplicationEnum(str, enum.Enum):
    APPLICATION_ID = "application_id"
    APPLICATION_DATE = "application_date"
    STATUS = "status"
    STUDENT_ID = "student_id"
    DRIVE_ID = "drive_id"