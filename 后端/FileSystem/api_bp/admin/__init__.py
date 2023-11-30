from flask import Blueprint
from api_bp.admin.user import user_bp
from api_bp.admin.classes import classes_bp

admin_bp=Blueprint('admin',__name__)

admin_bp.register_blueprint(user_bp)
admin_bp.register_blueprint(classes_bp)
