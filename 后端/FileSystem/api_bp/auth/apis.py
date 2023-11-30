import os
from io import BytesIO

from PIL import Image

from configs import COVER_FOLDER_URL
from data_base import Academy

from flask import Blueprint, request, jsonify, make_response
from utils.JWT import auth, verify_token, get_field

apis_bp=Blueprint('apis',__name__)
@apis_bp.route('/academy_list/<string:identity>', methods=['GET'])
def get_academy_list(identity):
    return Academy.get_academy_list(identity)

@apis_bp.route('/get_token_payload/<string:field>', methods=['GET'])
@auth.login_required
def get_token_payload(field):
    return jsonify({field:get_field(field)})

@apis_bp.route('/get_cover/<string:class_id>', methods=['GET'])
def get_cover(class_id):
    file_suffix=''
    for dirpath, dirnames, files in os.walk(COVER_FOLDER_URL):#遍历文件夹查找文件
        for file_name in files:
            if class_id in file_name:
                file_suffix = file_name.split('.')[1]
    image = Image.open(COVER_FOLDER_URL+class_id+'.'+file_suffix)
    buf = BytesIO()

    #设置文件类型
    file_type = file_suffix
    if file_type=='jpg':
        file_type='JPEG'

    image.save(buf, file_type)
    buf_str = buf.getvalue()
    response = make_response(buf_str)  # 把buf_str作为response返回前端，并设置首部字段
    response.headers['Content-Type'] = 'image/jpeg'

    return response