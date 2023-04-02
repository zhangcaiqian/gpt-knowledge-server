import os

from flask import Flask, request

from . import build_index, file_service


def main():
    build_index.initialize_index()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config['UPLOAD_FOLDER'] = './uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/query')
    def query_index():
        global index
        query_text = request.args.get("text", None)
        if query_text is None:
            return "No text found, please include a ?text=blah parameter in the URL", 400
        response = build_index.index.query(query_text)
        return str(response), 200
    
    @app.route('/', methods=['GET', 'POST'])
    def upload_file_handler():
        res = file_service.upload(app=app)
        return res

    return app

if __name__ == 'flaskr':
    main()