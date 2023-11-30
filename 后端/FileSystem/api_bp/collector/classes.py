from flask import Blueprint, jsonify, request


from data_base import User, Collection
from utils.JWT import auth, get_id, get_user_roles, get_token_from_request

classes_bp=Blueprint('classes',__name__)

@classes_bp.route('/get_class_list_collector', methods=['GET'])
@auth.login_required(role='collector')
def get_class_list():
    roles = get_user_roles(get_token_from_request(request))
    if 'teacher' in roles:
        class_list = User.teacher_get_class_list(get_id())
    elif 'student' in roles:
        class_list = User.student_get_permission_class_list(get_id())
    return jsonify(class_list)

@classes_bp.route('/get_collections_by_class_id', methods=['POST'])
@auth.login_required(role='collector')
def get_collections_by_class_id():
    class_id = request.form['class_id']
    collections = Collection.get_collections_by_class_id(class_id)
    return jsonify(collections)