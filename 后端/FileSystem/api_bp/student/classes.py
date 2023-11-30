import json
import os
from flask import Blueprint, jsonify, request


from configs import COLLECTIONS_FOLDER_URL
from data_base import Class, ClassStudentMap, User, Collection, CollectionItems, CollectionRecord
from utils.JWT import auth, get_id, get_user_roles, get_token_from_request, get_name

classes_bp=Blueprint('classes',__name__)

@classes_bp.route('/student_get_class_list', methods=['GET'])
@auth.login_required(role='student')
def get_class_list():
    return jsonify(User.student_get_class_list(get_id())), 200

@classes_bp.route('/student_join_class', methods=['POST'])
@auth.login_required(role='student')
def student_join_class():
    if Class.get_class(request.form['class_id']):
        ClassStudentMap.student_join_class(request.form['class_id'],get_id())
        return '',200
    else:
        return '',404

@classes_bp.route('/student_quit_class', methods=['POST'])
@auth.login_required(role='student')
def student_quit_class():
    ClassStudentMap.student_quit_class(request.form['class_id'],get_id())
    return '',200