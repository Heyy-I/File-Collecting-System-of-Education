import os
import time
from flask_httpauth import HTTPTokenAuth
from authlib.jose import jwt,JoseError
from configs import TOKEN_KEY, identity_permission_code_map

auth = HTTPTokenAuth(scheme='JWT')

def generate_auth_token(user, persist_second):
    header = {'typ': 'JWT',
              'alg': 'HS256'}
    now = int(time.time())

    claims  = {'iss': '班班集',
               'sub': 'AuthToken',
               'iat': now,
               'exp': now+persist_second,
               'id': user.id,
               'name': user.name,
               'AES-key' : os.urandom(16).hex(),
               'AES-iv' : os.urandom(16).hex(),
               'permission_code': user.get_permission_code()}
    return 'JWT '+jwt.encode(header, claims , TOKEN_KEY).decode('utf-8')

# 验证token
@auth.verify_token
def verify_token(token):
    try:
        if token[:3]=='JWT':
            token = token[4:]
        claims = jwt.decode(token, TOKEN_KEY)
        flag = True
        if(claims['exp'] < int(time.time())):
            flag = False
        return flag
    except JoseError:
        return False


@auth.get_user_roles
def get_user_roles(token):
    try:
        if type(token) != str:
            if token.get('token'):
                token = token['token']
        claims = jwt.decode(token, TOKEN_KEY)
        roles=[]
        p_code = claims['permission_code']
        for role, code in identity_permission_code_map.items():
            if p_code&code:
                roles.append(role)
        return roles
    except JoseError:
        return None


def get_token_from_request(request):
    return request.headers.get('Authorization')[4:]
def decode_token_from_text(token):
    if token[:3]=='JWT':
        token = token[4:]
    return jwt.decode(token, TOKEN_KEY)
def decode_token():
    return jwt.decode(auth.get_auth()['token'], TOKEN_KEY)

def get_field(field):
    return decode_token()[field]
def get_permission_code():
    return get_field('permission_code')
def get_id():
    return get_field('id')
def get_name():
    return get_field('name')
def get_aes_key():
    key = get_field('AES-key')
    return key[17:]+key[:17]
def get_aes_iv():
    iv = get_field('AES-iv')
    return iv[17:]+iv[:17]