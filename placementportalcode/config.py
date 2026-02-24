import os

class Config:
    BASEDIR=os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "dev-secret-key"
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(BASEDIR,"placement_portal.db")
    SQLALCHEMY_TRACK_MODIFICATIONS=False