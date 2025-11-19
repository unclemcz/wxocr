# -*- coding: utf-8 -*-

from flask import request, Blueprint,jsonify,redirect, url_for

from ..lib import  wxocr
from ..lib import  db


ocr = Blueprint('ocr',__name__,url_prefix='/ocr')

@ocr.route('/', methods=['GET', 'POST'])
@ocr.route('', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keycount = db.get_apikey_count()
        if keycount > 0:
            apikey = request.json.get('key')
            if db.is_apikey_exists(apikey):
                base64_img = request.json.get("image")
                return wxocr.ocr(base64_img)
            else:
                return jsonify({'errcode':-1,'msg':'apikey不存在'})
        else:
            base64_img = request.json.get("image")
            return wxocr.ocr(base64_img)
    elif request.method == 'GET':
        #跳转到/index页面
        return redirect(url_for('index.main'))
