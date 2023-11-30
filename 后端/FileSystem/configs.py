USERNAME = 'root'
PASSWORD = 'password'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'file_system'
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_ECHO = True

SAMPLE_FIELD="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
PROJECT_URL = "C:/Users/heyy/PycharmProjects/FileSystem/"
#项目路径
UPLOAD_FOLDER = PROJECT_URL+"fileSave/"
#上传文件的存储位置
COVER_FOLDER_URL = PROJECT_URL+'src/cover/'
#班级封面存储位置
COLLECTIONS_FOLDER_URL = PROJECT_URL+'collections/'

APP_IP = '192.168.31.95'
APP_PORT = 5432
FRONT_IP = APP_IP
FRONT_PORT = '8080'

ACTIVATE_CODE_LENGTH = 48
#邮箱激活码长度

identity_permission_code_map={'student'     :    0b1,
                              'collector'   :   0b10,
                              'teacher'     :  0b100,
                              'admin'       : 0b1000,
                              'super_admin' :0b11000,}

TOKEN_KEY = 'token_hly'
TOKEN_PERSIST_SECOND_LONG = 2592000 #一个月
TOKEN_PERSIST_SECOND_SHORT = 3600   #一小时

SCHEDULER_TIMEZONE = 'Asia/Shanghai'