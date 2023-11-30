import json
from datetime import timedelta
from os import urandom

from configs import APP_IP, APP_PORT, FRONT_IP, FRONT_PORT, UPLOAD_FOLDER, COLLECTIONS_FOLDER_URL, \
    SCHEDULER_TIMEZONE
from api_bp import api_bp
from flask import Flask, request, make_response

from data_base import Collection, remind_email, Class
from utils.AES import encrypt, decrypt, download_encrypt
from utils.my_email import zip_email
from utils.scheduler import scheduler, collection_packages_clear, one_day_forward

app = Flask(__name__, template_folder='src/templates')
app.secret_key = urandom(16)
app.register_blueprint(api_bp, url_prefix="/api")


#文件保存位置
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 最大上传文件大小   100MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1000 * 1000
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.config["SQLALCHEMY_POOL_RECYCLE"] = 850

@app.before_request
def before_request():
    white_list=['/api/'+url for url in ['verification','login','regist']]
    if request.method == 'POST':
        if request.path in white_list:
            request.form = json.loads(request.data.decode('utf-8'))
        else:
            if request.headers.get('enctype'):
                pass
            else:
                request.form = decrypt(request.data)




@app.after_request
def after_request(res):
    resp = make_response(res)
    res.headers['Access-Control-Allow-Origin'] = f'http://{FRONT_IP}:{FRONT_PORT}'
    res.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization,enctype,Content-Disposition"
    res.headers['Access-Control-Allow-Credentials'] = 'true'
    res.headers['Access-Control-Allow-Methods'] = "GET,POST,OPTIONS"#PUT,DELETE,
    res.headers['Access-Control-Expose-Headers'] = "Content-Disposition,Encryption-Algorithm"
    if request.headers.get('Authorization') and resp.data:
        res.headers['Encryption-Algorithm'] = "AES"
        if res.headers.get("Content-Disposition"):
            resp.data = download_encrypt(resp.data)
        else:
            resp.data = encrypt(resp.data)
    return resp

if __name__ == '__main__':
    #初始定时任务
    for collection in Collection.get_collections_end_in_future(one_day_=True):#任务截止前一天提醒
        scheduler.add_job(remind_email, id=collection.collection_id, trigger='date', run_date=one_day_forward(collection.collection_end_time), args=[collection],
                          timezone=SCHEDULER_TIMEZONE)
    # for collection in Collection.get_collections_end_in_future(one_day_=False):
    #     class_ = Class.get_class(collection.class_id)
    #     collector_id_list=[]
    #     collector_id_list.append(class_.teacher_id)
    #     collector_id_list.extend(class_.permission_students_id.split(','))
    #     file_path = COLLECTIONS_FOLDER_URL + 'packages/' + collection.collection_id + '.zip'
    #     file_name= collection.class_name + '  ' + collection.collection_name
    #     scheduler.add_job(zip_email, id=collection.collection_id+'.zip', trigger='date',
    #                       run_date=collection.collection_end_time, kwargs={'to_address':collector_id_list,'zip_file':{'file_path':file_path, 'file_name':file_name,'class_name':collection.class_name,'collection_name':collection.collection_name}},
    #                       timezone=SCHEDULER_TIMEZONE)
    scheduler.add_job(collection_packages_clear, 'interval', hours=6, timezone=SCHEDULER_TIMEZONE)

    scheduler.start()
    app.run(host=APP_IP, port=APP_PORT, debug=True, threaded=True)