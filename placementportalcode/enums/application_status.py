import enum

class ApplicationStatusEnum(enum.Enum):
    APPLIED='applied'
    SHORTLISTED='shortlisted'
    SELECTED='selected'
    REJECTED='rejected'
    WAITLISTED='waitlisted'
    HIRED='hired'