from flask import Blueprint, request, jsonify

from utils.JWT import generate_auth_token, verify_token, decode_token_from_text
from data_base import User
from utils.notify import notify
from configs import TOKEN_PERSIST_SECOND_LONG, TOKEN_PERSIST_SECOND_SHORT

login_bp=Blueprint('login',__name__)

@login_bp.route('/login', methods=['POST'])
def login():
    id = request.form['id']
    password = request.form['password']

    user = User.login(id=id, password=password)
    if user:
        if request.form['remember_me']:
            token = generate_auth_token(user, TOKEN_PERSIST_SECOND_LONG)
        else:
            token = generate_auth_token(user, TOKEN_PERSIST_SECOND_SHORT)
        claims = decode_token_from_text(token)
        return jsonify({'token': token, 'key':claims['AES-key'], 'iv':claims['AES-iv'], 'title': '登录成功', 'message': ''}),200
    else:
        return notify('登录失败',"用户名或密码错误"), 210

@login_bp.route('/auto_login', methods=['GET'])
def auth_verify():
    if verify_token(request.headers.get('Authorization')):
        return '',200
    else:
        return '',201