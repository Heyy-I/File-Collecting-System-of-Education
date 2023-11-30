from flask import Blueprint
from api_bp.collector.classes import classes_bp
from api_bp.collector.collections import collections_bp


collector_bp=Blueprint('collector',__name__)


collector_bp.register_blueprint(classes_bp)
collector_bp.register_blueprint(collections_bp)