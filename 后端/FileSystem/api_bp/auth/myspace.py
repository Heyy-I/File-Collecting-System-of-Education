from random import sample

from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from configs import SAMPLE_FIELD, ACTIVATE_CODE_LENGTH
from data_base import User, session, User_n
from utils.JWT import auth, get_id
from utils.my_email import email_confirm_email, password_confirm_email

myspace_bp=Blueprint('myspace',__name__)

@myspace_bp.route('/get_my_info', methods=['GET'])
@auth.login_required
def get_my_info():
    user=User.get_user(get_id()).to_dict()
    user.pop('password')
    return user,200


@myspace_bp.route('/change_name', methods=['POST'])
@auth.login_required
def change_name():
    User.get_user(get_id()).update('name',request.form['name'])
    return '',200

@myspace_bp.route('/change_password', methods=['POST'])
@auth.login_required
def change_password():
    activate_code = ''.join(sample(SAMPLE_FIELD, ACTIVATE_CODE_LENGTH))
    print(request.form)
    user = User.login(id=get_id(), password=request.form['old_password'])
    if user:
        user.password=generate_password_hash(request.form['new_password'])
        User_n.new_from_user(user,activate_code)
        password_confirm_email(user.email,activate_code)
        return '',200
    else:
        return '',401
@myspace_bp.route('/change_email', methods=['POST'])
@auth.login_required
def change_email():
    if session.query(User).filter(User.email == request.form['email']).first():
        return '邮箱已被占用', 212
    activate_code = ''.join(sample(SAMPLE_FIELD, ACTIVATE_CODE_LENGTH))
    user = User.get_user(get_id())
    old_email=user.email
    user.email = request.form['email']
    User_n.new_from_user(user,activate_code)
    email_confirm_email(old_email,activate_code)
    return '',200