from random import randint,sample


from io import BytesIO
from PIL  import Image, ImageFont, ImageDraw
from flask import Blueprint, make_response, session, request

from configs import SAMPLE_FIELD

captcha_bp=Blueprint('captcha',__name__)


@captcha_bp.route('/verification', methods=['POST'])#验证码
def verification():
    user_captcha = request.form['captcha'].lower()
    real_captcha = session.get('captcha')
    if user_captcha == real_captcha:
        return '验证码校验成功', 200
    else:
        return '验证码校验失败', 201

@captcha_bp.route('/captcha/<float:v>', methods=['GET'])
def captcha(v):
    image, code = get_captcha()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)# 把buf_str作为response返回前端，并设置首部字段
    response.headers['Content-Type'] = 'image/jpeg'

    # 将验证码字符串储存在session中
    session['captcha'] = code.lower()
    return response


def random_color():
    return (randint(64, 192), randint(64, 192), randint(64, 255))

def draw_lines(draw, num, width, height):
    for i in range(num):
        x1 = randint(0, int(width*0.666))
        y1 = randint(0, height / 2)
        x2 = randint(int(width*0.333), width)
        y2 = randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill=random_color(), width=1)

def get_captcha():
    code = ''.join(sample(SAMPLE_FIELD, 4))
    # 图片大小
    width, height = 100, 38
    # 新图片对象
    im = Image.new('RGB', (width, height), '#fcfcfc')
    # 字体
    font = ImageFont.truetype('app/static/font/ariali.ttf', 30)
    # draw对象
    draw = ImageDraw.Draw(im)

    # 绘制字符串
    for item in range(4):
        draw.text(xy=(5 + randint(-3, 3) + 23 * item, 3 + randint(-4, 4)),text=code[item], fill=random_color(), font=font)
    # 添加扰乱线
    # draw_lines(draw, 4, width, height)
    for i in range(3):
        draw.line([(0,randint(0, height)),(width,randint(0, height))],fill=random_color() , width=2)
    #添加噪点
    for i in range(int(width*height*0.01)):
        draw.point([randint(0, width), randint(0, height)], fill=random_color())
        x = randint(0, width)
        y = randint(0, height)
        draw.arc((x, y, x + 4, y + 1), 0, 90, fill=random_color())
    return im, code