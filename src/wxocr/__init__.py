# src/my_flask_app/__init__.py
from flask import Flask

from .route.ocr import ocr
from .route.index import index


def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False # 解决中文乱码问题
    app.register_blueprint(ocr)
    app.register_blueprint(index)

    from .lib import db 
    db.init_app(app)

    return app

