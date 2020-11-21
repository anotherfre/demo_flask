# -*- coding: utf-8 -*-
from app.web_api import *


@admin.route('/')
def index():
    print(1)
    return render_template('index.html')


@admin.route('/pic')
def pic():
    return json.dumps({'ret': 0, 'status': 'success', 'msg': '晚上好'})


@admin.route('/music')
def music():
    return json.dumps({'ret': 0, 'status': 'success', 'msg': '早上好'})


@admin.route('/book')
def book():
    return json.dumps({'ret': 0, 'status': 'success', 'msg': '中午好'})



