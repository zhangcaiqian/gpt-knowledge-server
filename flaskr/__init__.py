import os
import threading

from flask import Flask, request
from flask_socketio import SocketIO, emit

from . import file_service, index_service, utils


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config['UPLOAD_FOLDER'] = './documents'
    app.config['INDEX_FILE_FOLDER'] = './file_index'
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1000 * 1000

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
        return utils.resp_format(data={'answer': str(response)}, msg='success')
    
    @app.route('/', methods=['GET'])
    def home():
        return '首页'
    
    @app.route('/upload', methods=['POST'])
    def handle_upload():
        if 'file' not in request.files:
            return utils.resp_format(msg='No file part', code=400)
        # 获取文件名和保存路径
        file = request.files['file']
        if file.filename == '':
            return utils.resp_format(msg='No selected file', code=400)
        
        if not file_service.allowed_file(file.filename):
            return utils.resp_format(msg='File type not allowed', code=400)
        
        filename = file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 创建新线程上传文件
        t = threading.Thread(target=upload_file, args=(file, save_path))
        t.start()
        t.join()
        # 生成文件向量索引
        msg = index_service.gen_index_with_pdf(file.filename)

        return utils.resp_format(msg='success',data={'file': filename, 'vector': msg})

    def upload_file(file, save_path):
        # 保存文件
        file.save(save_path)
        # 生成文件向量索引
        index_service.gen_index_with_pdf(file.filename)

        # 向客户端发送上传完成消息
        socketio.emit('upload_complete', {'filename': save_path})
    
    @app.route('/files')
    def list_files():
        # 获取目录路径
        dir_path = app.config['INDEX_FILE_FOLDER']

        # 获取目录下所有文件名
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

        # 返回文件列表
        return utils.resp_format(data={'files': files}, msg='success')

    return app

if __name__ == 'flaskr':
    print('flaskr is available, GPT knowledge is available')