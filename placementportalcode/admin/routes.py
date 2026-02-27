from flask import Blueprint,render_template,session,redirect,url_for
from http import HTTPMethod 
from flask import request
from placementportalcode.models import User
from placementportalcode.enums.role import RoleEnum
from placementportalcode.enums.modelsenum import UserEnum
admin_bp=Blueprint("admin",__name__,url_prefix="/admin")

@admin_bp.route("/dashboard",methods=[HTTPMethod.GET] )
def dashboard():
    user_id=session.get("user_id")
    if not user_id:
        return redirect(url_for("auth.login"))
    user=User.query.get(user_id)
    if not user:
        return redirect(url_for("auth.login"))
    if user.role!=RoleEnum.ADMIN.value:
        return redirect(url_for("auth.login"))
    
    
    if(request.method==HTTPMethod.GET):
        return render_template("admin/dashboard.html")
    

    return "Admin Dashboard"
