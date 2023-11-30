import os

from flask import Blueprint, jsonify, request

from configs import PROJECT_URL, COVER_FOLDER_URL
from data_base import Class, ClassStudentMap, User
from utils.JWT import auth, get_id

classes_bp=Blueprint('classes',__name__)


@classes_bp.route('/get_class_info/<string:class_id>', methods=['GET'])
@auth.login_required(role='teacher')
def get_class_info(class_id):
    class_info = Class.get_class_info(class_id)
    return jsonify(class_info)

@classes_bp.route('/teacher_get_class_list', methods=['GET'])
@auth.login_required(role='teacher')
def get_class_list():
    class_list = User.teacher_get_class_list(get_id())
    return jsonify(class_list)

@classes_bp.route('/cover_upload', methods=['POST'])
@auth.login_required(role='teacher')
def cover_upload():
    file = request.files['file']
    filename = request.form['class_id']+'.'+file.filename.split('.')[1]
    file.save(PROJECT_URL+'src/cover/'+filename)
    return '',200

@classes_bp.route('/update_class', methods=['POST'])
@auth.login_required(role='teacher')
def class_update():
    field = request.form['field']
    class_id  = request.form['class_id']
    data = request.form[field]
    Class.update(class_id, field, data)
    return '',200

@classes_bp.route('/student_adjust', methods=['POST'])
@auth.login_required(role='teacher')
def student_adjust():
    class_id = request.form['class_id']
    student_id_list = request.form['student_id_list']
    flag = request.form['flag']
    Class.student_adjust(class_id, student_id_list, flag)
    return '',200

@classes_bp.route('/delete_class', methods=['POST'])
@auth.login_required(role='teacher')
def delete_class():
    class_id = request.form['class_id']
    Class.get_class(class_id).delete()
    file_suffix = ''
    for dirpath, dirnames, files in os.walk(COVER_FOLDER_URL):  # 遍历文件夹查找文件
        for file_name in files:
            if class_id in file_name:
                file_suffix = file_name.split('.')[1]
    if file_suffix:
        file_path = COVER_FOLDER_URL + class_id + '.' + file_suffix
        os.remove(file_path)
    return '',200

@classes_bp.route('/create_class', methods=['POST'])
@auth.login_required(role='teacher')
def create_class():
    class_name = request.form['class_name']
    Class.new_class(class_name, get_id())
    return '', 200