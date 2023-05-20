import os

from flask import send_from_directory

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'html', 'json', 'md', 'xml'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def download_file(name=None, app=None):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)