from flask import Blueprint
from api_bp.student.collections import collections_bp
from api_bp.student.classes import classes_bp

student_bp=Blueprint('student',__name__)


student_bp.register_blueprint(collections_bp)
student_bp.register_blueprint(classes_bp)