# -*- coding: utf-8 -*-

from flask import  Blueprint


index = Blueprint('index',__name__,url_prefix='/')

@index.route('/', methods=['GET'])
@index.route('/index', methods=['GET'])
def main():
    return '首页'