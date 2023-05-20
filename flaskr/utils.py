from flask import jsonify


def resp_format(data={}, msg='', code=200):
    return jsonify({'message': msg, 'data': data}), code