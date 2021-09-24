# -*- coding: utf-8 -*-
from app.web_api import *


@admin.route('/')
def index():
    return render_template('new_index.html')


@admin.route('/get_cont', methods=['GET', 'POST'])
def get_cont():
    conn = get_connection()
    if not conn:
        return json.dumps({'ret': -1, 'msg': '数据库连接失败'})
    try:
        with conn.cursor() as cursor:
            sql = """select content from user_contents where del_flag=0 ORDER BY RAND() limit 1"""
            if cursor.execute(sql):
                query_data = cursor.fetchone()
                content = query_data.get('content', '')
            data = {
                "ret": 0,
                "data": content
            }
            return json.dumps(data)
    except Exception as e:
        print(traceback.format_exc())
        return json.dumps({'ret': -3, 'msg': '操作异常'})


@admin.route('/publish', methods=['GET', 'POST'])
def publish():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            content = request.form.get('content', '')
            user_id = request.form.get('user_id', 0)
            if not content:
                return json.dumps({'ret': -2, 'status': 'failed', 'msg': '请填写内容'})
            create_time = datetime.datetime.now()
            sql = ''' insert into user_contents (user_id, content,create_time,del_flag)values(%s,%s,%s, 0)'''
            cursor.execute(sql, (user_id, content, create_time))
            conn.commit()
            return json.dumps({'ret': 0, 'msg': '发送成功'})
    except:
        print(traceback.format_exc())
        return json.dumps({'ret': -3, 'status': 'failed'})
    finally:
        conn.close()
