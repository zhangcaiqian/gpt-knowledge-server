import os

from flask import jsonify


def resp_format(data={}, msg='', code=200):
    return jsonify({'message': msg, 'data': data}), code

def get_name_without_suffix(filename):
    return os.path.splitext(filename)[0]
