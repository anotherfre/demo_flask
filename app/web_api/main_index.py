# -*- coding: utf-8 -*-
from app.web_api import *


@admin.route('/')
def index():
    return render_template('index.html')


@admin.route('/get_cont/<page>', methods=['GET', 'POST'])
def get_cont(page):
    conn = get_connection()
    if not conn:
        return json.dumps({'ret': -1, 'msg': '数据库连接失败'})
    try:
        with conn.cursor() as cursor:
            if int(page) > 10:
                return json.dumps({"ret": -2, "data": []})
            sql = ''' select content from user_contents where del_flag=0 order by create_time desc'''
            sql += ' limit {page}, {limit}'.format(page=(int(page) - 1) * 10, limit=10)
            result = []
            if cursor.execute(sql):
                query_data = cursor.fetchall()
            else:
                return json.dumps({"ret": -2, "data": []})

            for query in query_data:
                result.append({'result': query.get('content')})
            data = {
                "ret": 0,
                "data": result
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
