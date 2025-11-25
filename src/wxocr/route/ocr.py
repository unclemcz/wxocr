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
        return render_template('ocr.html')

@ocr.route('/demo', methods=['POST'])
def demo():
    """
    OCR演示接口，用于在线识别功能
    不需要验证key，但限制图片大小
    """
    if not request.is_json:
        return jsonify({'errcode':-1,'msg':'请使用json格式提交数据'})

    if not request.get_json():
        return jsonify({'errcode':-1,'msg':'json格式错误'})

    if not request.json.get("image"):
        return jsonify({'errcode':-1,'msg':'缺少image参数'})

    # 获取图片数据
    base64_img = request.json.get("image")

    # 检查图片大小（限制为原始文件15KB）
    try:
        # 如果包含data:image前缀，则去除前缀后检查大小
        if base64_img.startswith("data:image/"):
            base64_data = base64_img.split(";base64,")[-1]
        else:
            base64_data = base64_img

        # 计算原始文件大小（base64解码后的大小）
        original_size = len(base64_data) * 3 // 4  # base64解码后的原始大小

        if original_size > 15 * 1024:  # 15KB
            return jsonify({
                'errcode':-1,
                'msg':f'图片文件大小不能超过15KB，当前大小约为{original_size/1024:.1f}KB'
            })

    except Exception as e:
        return jsonify({'errcode':-1,'msg':'图片数据格式错误'})

    # 执行OCR识别
    return wxocr.ocr(base64_img)
