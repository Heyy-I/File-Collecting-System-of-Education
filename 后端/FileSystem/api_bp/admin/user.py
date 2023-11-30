from flask import Blueprint, request, jsonify

from data_base import User, User_n
from utils.JWT import auth, get_id

user_bp=Blueprint('user',__name__)

@user_bp.route('/admin_get_user_list', methods=['GET'])
@auth.login_required(role=['admin'])
def admin_get_user_list():
    return jsonify(User.admin_get_user_list(get_id())),200

@user_bp.route('/reset_user_password', methods=['POST'])
@auth.login_required(role=['admin'])
def reset_user_password():
    return jsonify(User.get_user(request.form['id']).reset_password()),200

@user_bp.route('/delete_user', methods=['POST'])
@auth.login_required(role=['admin'])
def delete_user():
    User.get_user(request.form['id']).delete()
    return '',200


###################################################################################
@user_bp.route('/get_unactivated_user', methods=['GET'])
@auth.login_required(role=['admin'])
def get_unactivated_user():
    return jsonify(User.get_user(get_id()).get_unactivated_user()),200

@user_bp.route('/activate_permission_user', methods=['POST'])
@auth.login_required(role=['admin'])
def activated_user():
    User_n.activate_permission_user(request.form['activate_code'])
    return '',200

