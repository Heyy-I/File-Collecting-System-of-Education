from flask import jsonify


def notify(title, message):
    return jsonify({'title': title, 'message': message})