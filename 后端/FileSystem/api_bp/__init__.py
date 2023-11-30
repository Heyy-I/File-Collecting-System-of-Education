from flask import Blueprint

from api_bp.admin import admin_bp
from api_bp.auth import auth_bp
from api_bp.teacher import teacher_bp
from api_bp.collector import collector_bp
from api_bp.student import student_bp

api_bp=Blueprint('api_bp',__name__)

api_bp.register_blueprint(admin_bp)
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(teacher_bp)
api_bp.register_blueprint(collector_bp)
api_bp.register_blueprint(student_bp)