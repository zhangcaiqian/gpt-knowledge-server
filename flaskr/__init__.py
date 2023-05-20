import os
import threading

from flask import Flask, request
from flask_socketio import SocketIO, emit

from . import file_service, index_service


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config['UPLOAD_FOLDER'] = './documents'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    socketio = SocketIO(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    socketio.run(app)

    @app.route('/alive')
    def hello():
        return 'Hello, my friends!'

    @app.route('/query')
    def query_index():
        global index
        query_text = request.args.get("text", None)
        query_index_name = request.args.get("index", None)
        if query_text is None:
            return "No text found, please include a ?text=blah parameter in the URL", 400
        if query_index_name is None or query_index_name == "":
            return "No index found, please include a ?index=blah parameter in the URL", 400
        index = index_service.load_index_from_disk(query_index_name)
        response = index.query(query_text)
        return str(response), 200
    
    @app.route('/', methods=['GET', 'POST'])
    def upload_file_handler():
        res = file_service.upload(app=app)
        return res
    
    @app.route('/upload', methods=['POST'])
    def handle_upload():
        # 获取文件名和保存路径
        file = request.files['file']
        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 创建新线程上传文件
        t = threading.Thread(target=upload_file, args=(file, save_path))
        t.start()

        return 'OK'

    def upload_file(file, save_path):
        # 保存文件
        file.save(save_path)

        # 向客户端发送上传完成消息
        socketio.emit('upload_complete', {'filename': save_path})

    return app

if __name__ == 'flaskr':
    print('flaskr is available, GPT knowledge is available')