from io import BytesIO

from PIL import Image
from flask import make_response

from configs import PROJECT_URL


def get_image(path):
    image = Image.open(rf'{PROJECT_URL}{path}')
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)  # 把buf_str作为response返回前端，并设置首部字段
    response.headers['Content-Type'] = 'image/jpeg'
    return response

def get_cover(class_id):
    return get_image(rf'src/cover/templates/{class_id}.jpeg')