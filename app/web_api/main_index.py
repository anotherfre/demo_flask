# -*- coding: utf-8 -*-
from app.web_api import *


@admin.route('/')
def index():
    print(1)
    return render_template('index.html')


@admin.route('/pic')
def pic():
    return json.dumps({'ret': 0, 'status': 'success', 'msg': '图片'})



