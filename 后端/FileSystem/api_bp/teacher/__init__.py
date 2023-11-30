from flask import Blueprint
from api_bp.teacher.classes import classes_bp

teacher_bp=Blueprint('teacher',__name__)


teacher_bp.register_blueprint(classes_bp)
