# -*- coding: utf-8 -*-

from flask import request, Blueprint,jsonify,render_template

from ..lib import  wxocr
from ..lib import  db


ocr = Blueprint('ocr',__name__,url_prefix='/ocr')

@ocr.route('/', methods=['GET', 'POST'])
@ocr.route('', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'errcode':-1,'msg':'请使用json格式提交数据'})
        if not request.get_json():
            return jsonify({'errcode':-1,'msg':'json格式错误'})
        if not request.json.get("image"):
            return jsonify({'errcode':-1,'msg':'缺少image参数'})
        keycount = db.get_apikey_count()
        if keycount > 0:
            apikey = request.json.get('key')
            if not apikey:
                return jsonify({'errcode':-1,'msg':'缺少key参数'})
            
            if db.is_apikey_exists(apikey):
                base64_img = request.json.get("image")
                return wxocr.ocr(base64_img)
            else:
                return jsonify({'errcode':-1,'msg':'apikey不存在'})
        else:
            base64_img = request.json.get("image")
            return wxocr.ocr(base64_img)
    elif request.method == 'GET':
        return render_template('index.html')
