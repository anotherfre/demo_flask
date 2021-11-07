# -*- coding: utf-8 -*-
from web_api import *


class UserContent:
    def __init__(self, u_request=None, u_session=None, u_conn=None):
        self.request = u_request
        self.session = u_session
        self.conn = u_conn
        self.args = u_request.args
        self.form = u_request.form

    def run(self):
        option = self.args.get('type')
        if not hasattr(self, option):
            return 'failed', 500
        result = getattr(self, option)()
        return result

    def push_content(self):
        nickname = self.form.get('nickname')
        content = self.form.get('content')
        create_time = datetime.datetime.utcnow()
        if len(content) > 255:
            return 'content to long', 200
        with self.conn.cursor() as cursor:
            sql = '''insert into user_content(nickname, content, create_time,del_flag) values(%s, %s,%s, 0)'''
            cursor.execute(sql, (nickname, content, create_time))
            self.conn.commit()
            return 'push_content', 200


@admin.route('/user_content', methods=['GET', 'POST'])
def user_content():
    conn = get_connection()
    if not conn:
        return 'conn failed', 500
    try:
        _user_content = UserContent(request, session, conn)
        result = _user_content.run()
        return result
    except Exception as e:
        return 'error', 500
    finally:
        conn.close()
