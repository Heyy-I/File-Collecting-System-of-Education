import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from io import open
from configs import PROJECT_URL, APP_IP, APP_PORT, FRONT_IP, FRONT_PORT

__my_address = '2483497688@qq.com'  # 发件人邮箱账号
# my_pass = 'ngmuuvinfkrqbdgc'  # 发件人邮箱授权码  9947
__my_pass = 'bgtiwcbipgctdhgf'  # 发件人邮箱授权码  2483


def regist_email(to_address,code):
    mail('注册邮箱验证', to_address, templates('regist').replace('CODE', code))
def email_confirm_email(to_address,code):
    mail('绑定邮箱修改验证', to_address, templates('email_confirm').replace('CODE', code))
def password_confirm_email(to_address,code):
    mail('密码修改验证', to_address, templates('password_confirm').replace('CODE', code))

def zip_email(to_address,zip_file):
    zip_file['file_name']=zip_file['file_name']+'.zip'
    mail('文件收集完成', to_address, templates('zip')
         .replace('CLASS_NAME', zip_file['class_name'])
         .replace('COLLECTION_NAME', zip_file['collection_name']),files=[zip_file])

def templates(type):
    with open(PROJECT_URL+f'/src/templates/email/{type}.html',encoding = "utf-8") as f:
        html_template = f.read().replace('APP_IP',APP_IP).replace('APP_PORT',str(APP_PORT)).replace('FRONT_IP',FRONT_IP).replace('FRONT_PORT',FRONT_PORT)
    return html_template

def annex(file_path, file_name=''):
    if file_name == '':
        file_name = file_path[file_path.rfind('/'):len(file_path)]
    annex = MIMEApplication(open(file_path, 'rb').read())
    annex.add_header('Content-Disposition', 'attachment', filename=file_name)
    return annex

def mail(subject, to_address, html_template, files=[]):
    msg = MIMEMultipart()
    msg.attach(MIMEText(html_template, 'html', 'utf-8'))
    msg['Subject'] = subject  # 邮件标题
    msg['From'] = formataddr(["班班集", __my_address])
    msg['Cc'] = ''#抄送人

    for f in files:
        msg.attach(annex(f['file_path'], f['file_name']))

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(__my_address, __my_pass)
    server.sendmail(__my_address, to_address, msg.as_string())
    server.quit()  # 关闭连接
