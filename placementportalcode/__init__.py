from flask import Flask,render_template,redirect,url_for
from .extensions import db
from placementportalcode.auth.routes import auth_bp
from placementportalcode.admin.routes import admin_bp
from placementportalcode.company.routes import company_bp
from placementportalcode.student.routes import student_bp
from .config import Config
from flask_migrate import Migrate
import os

def create_app():
    app=Flask(__name__)
   

    app.config.from_object(Config)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)

    UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads", "resumes")
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    db.init_app(app)

    migrate = Migrate(app, db)

    from .models import User,Company,Application,PlacementDrive

    @app.route("/")
    def home():
        return redirect(url_for('auth.login'))
    return app

