import enum

class DriveApprovalStatusEnum(enum.Enum):
    APPROVED='approved'
    CLOSED='closed'
    PENDING='pending'


class CompanyEnumStatus(enum.Enum):
    PENDING='pending'
    APPROVED='approved'
    BLACKLISTED='blacklisted'
    