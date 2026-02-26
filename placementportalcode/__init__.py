from flask import Flask
from .extensions import db
from placementportalcode.auth.routes import auth_bp
from placementportalcode.admin.routes import admin_bp
from .config import Config
def create_app():
    app=Flask(__name__)

    app.config.from_object(Config)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    db.init_app(app)

    from .models import User,Company,Application,PlacementDrive

    @app.route("/")
    def home():
        return "Placement Portal Running"
    
    return app

