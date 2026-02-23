from flask import Flask
from .extensions import db
from .config import Config
def create_app():
    app=Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from .models import User,Quiz,Subject,Chapter,Scores

    @app.route("/")
    def home():
        return "Quiz Master Running"
    
    return app

