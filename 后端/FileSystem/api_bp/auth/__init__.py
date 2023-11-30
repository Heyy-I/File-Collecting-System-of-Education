from flask import Blueprint
from api_bp.auth.captcha import captcha_bp
from api_bp.auth.regist import regist_bp
from api_bp.auth.login import login_bp
from api_bp.auth.apis import apis_bp
from api_bp.auth.myspace import myspace_bp

auth_bp=Blueprint('auth',__name__)

auth_bp.register_blueprint(captcha_bp)
auth_bp.register_blueprint(regist_bp)
auth_bp.register_blueprint(login_bp)
auth_bp.register_blueprint(apis_bp)
auth_bp.register_blueprint(myspace_bp)