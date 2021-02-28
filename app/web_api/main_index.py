# -*- coding: utf-8 -*-
from app.web_api import *


@admin.route('/')
def index():
    return render_template('index.html')


@admin.route('/pic')
def pic():
    print(request.remote_addr)
    return json.dumps({'ret': 0, 'status': 'success', 'msg': '晚上好'})


@admin.route('/music')
def music():
    print(request.remote_addr)
    return json.dumps({'ret': 0, 'status': 'success', 'msg': '早上好'})


@admin.route('/book')
def book():
    print()
    print(request.remote_addr)
    return json.dumps({'ret': 0, 'status': 'success', 'msg': '中午好'})


@admin.route('/get_cont', methods=['GET', 'POST'])
def get_cont():
    conn = get_connection()
    if not conn:
        return json.dumps({'ret': -1, 'msg': '数据库连接失败'})
    try:
        with conn.cursor() as cursor:
            sql = ''' select content from user_contents where del_flag=0 order by rand() limit 1'''
            result = []
            if cursor.execute(sql):
                result = cursor.fetchone()['content']
            data = {
                "ret": 0,
                "data": result
            }
            return json.dumps(data)
    except Exception as e:
        print(traceback.format_exc())
        return json.dumps({'ret': -3, 'msg': '操作异常'})

