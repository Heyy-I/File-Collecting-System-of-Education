import json
import os
from flask import Blueprint, jsonify, request


from configs import COLLECTIONS_FOLDER_URL
from data_base import Class, ClassStudentMap, User, Collection, CollectionItems, CollectionRecord
from utils.JWT import auth, get_id, get_user_roles, get_token_from_request, get_name

collections_bp=Blueprint('collections',__name__)

@collections_bp.route('/get_collection_list', methods=['GET'])
@auth.login_required(role='student')
def get_student_collection_list():
    return Collection.get_student_collection_list(get_id()), 200

@collections_bp.route('/get_collection_items', methods=['POST'])
@auth.login_required(role='student')
def get_collection_items():
    return jsonify(CollectionItems.get_collection_items(get_id(),request.form['collection_id'])), 200


@collections_bp.route('/collection_upload', methods=['POST'])
@auth.login_required(role='student')
def collection_upload():
    file = request.files['file']
    item = json.loads(request.form['item'])
    path = COLLECTIONS_FOLDER_URL + item['collection_id'] + '/' + str(item['index']) + '_'+ item['info'] + '/' + get_id() + '_' + get_name() +'.'+file.filename.split('.')[1]
    file.save(path)
    CollectionRecord.new_collection_record({'collection_id':item['collection_id'],'index':item['index'],'student_id':get_id(),'student_name':get_name(),'submit_content':path})
    return '',200

@collections_bp.route('/roll_back', methods=['POST'])
@auth.login_required(role='student')
def roll_back():
    record = CollectionRecord.query_record(get_id(), request.form['collection_id'], request.form['index'])
    os.remove(record.submit_content)
    CollectionRecord.delete_record(get_id(), request.form['collection_id'], request.form['index'])
    return '',200
