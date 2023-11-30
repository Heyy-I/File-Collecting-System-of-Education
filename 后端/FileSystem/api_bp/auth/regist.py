from random import sample

from flask import Blueprint, request, render_template
from werkzeug.security import generate_password_hash

from data_base import session,User_n,User
regist_bp=Blueprint('regist',__name__)

from configs import ACTIVATE_CODE_LENGTH, SAMPLE_FIELD
from utils.my_email import regist_email
from utils.notify import notify
@regist_bp.route('/regist', methods=['POST'])
def regist():
    form = request.form
    name = form['name']
    password = form['password']
    email = form['email']
    academy = form['academy']
    identity = form['identity']
    if identity=='student':
        id = form['student_id']
    elif identity=='teacher':
        id = form['teacher_id']

    if session.query(User).filter(User.id == id).first():
        return notify('注册失败','该账号已被注册！'), 211
    if session.query(User).filter(User.email == email).first():
        return notify('注册失败','该邮箱已被注册！'), 212

    activate_code = ''.join(sample(SAMPLE_FIELD, ACTIVATE_CODE_LENGTH))
    session.add(User_n(id, name, generate_password_hash(password), email, academy, identity, activate_code))#附带激活码存入未激活用户表中
    regist_email(email,activate_code)
    session.commit()
    return notify('注册成功','请前往邮箱激活您的账号')

@regist_bp.route('/reactivate/password_confirm/<string:code>', methods=['GET'])
@regist_bp.route('/reactivate/email_confirm/<string:code>', methods=['GET'])
@regist_bp.route('/regist/activate/<string:code>', methods=['GET'])
def activate(code):
    # 验证准许激活状态与激活码
    user_query = session.query(User_n).filter(User_n.activate_code == code)
    if user_query.first():#激活码验证正确
        user_query.update({'activate_code': ''},synchronize_session=False)
        session.commit()
        User_n.activate_user()
        action=''
        if '/regist/activate/' in request.path:
            action='激活账号'
        elif '/reactivate/password_confirm/' in request.path:
            action='修改密码'
        elif '/reactivate/email_confirm/' in request.path:
            action='修改邮箱'
        return render_template('behavior_notify.html',action=action), 200
    return '',400