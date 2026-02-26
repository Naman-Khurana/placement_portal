from flask import Blueprint,render_template
from http import HTTPMethod 
from flask import request
admin_bp=Blueprint("admin",__name__,url_prefix="/admin")

@admin_bp.route("/dashboard",methods=[HTTPMethod.GET] )
def dashboard():
    if(request.method==HTTPMethod.GET):
        return render_template("admin/dashboard.html")
    return "Admin Dashboard"
