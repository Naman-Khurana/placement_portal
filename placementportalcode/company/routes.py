from flask import Flask ,Blueprint,session,render_template,redirect,url_for,request
from placementportalcode.models import Company,User
from placementportalcode.enums.role import RoleEnum
from http import HTTPMethod

company_bp=Blueprint("company",__name__,url_prefix="/company")

@company_bp.route("/dashboard",methods=[HTTPMethod.GET] )
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
        return render_template("company/dashboard.html")
    

    return "Admin Dashboard"