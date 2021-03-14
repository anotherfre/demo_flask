# -*- coding: utf-8 -*-
from app.web_api import *
import random
from app.web_api.gua_data import *
import xmltodict


def get_str_sha1_secret_str(res):
    import hashlib
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(res.encode('utf-8'))
    encrypts = sha.hexdigest()
    return encrypts


@admin.route('/')
def index():
    return render_template('index.html')


@admin.route('/pic', methods=['GET'])
def pic():
    try:
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")
        token = 'ldhlmclyhblsqt'
        sortlist = [token, timestamp, nonce]
        sortlist.sort()
        token = get_str_sha1_secret_str("".join(sortlist))

        if token == signature:
            return 'True'
        else:
            return "False"
    except:
        print(traceback.format_exc())


@admin.route('/pic', methods=['POST'])
def pic_post():
    try:
        openid = request.args.get("openid", '')
        rand_num = random.choice(list(baguaguaxiang))
        rand_xiang = baguaguaxiang[rand_num]
        liu_yao = 'i_' + gua_yao[rand_num[0]] + gua_yao[rand_num[1]]
        xiang_ci = solution_dict[liu_yao]
        data = request.data
        return_content = '''<xml>
                                          <ToUserName><![CDATA[%s]]></ToUserName>
                                          <FromUserName><![CDATA[gh_93df1f1728b5]]></FromUserName>
                                          <CreateTime>12345678</CreateTime>
                                          <MsgType><![CDATA[text]]></MsgType>
                                          <Content><![CDATA[%s]]></Content>
                                    </xml>'''
        if data:
            data = xmltodict.parse(request.data)['xml']
        else:
            data = ''
        content = data.get('Content')
        if content == '积水':
            return_content = return_content % (openid, ' 嘿！ 积水！！！')
        elif content == '卦':
            return_content = '''<xml>
                                  <ToUserName><![CDATA[%s]]></ToUserName>
                                  <FromUserName><![CDATA[%s]]></FromUserName>
                                  <CreateTime>12345678</CreateTime>
                                  <MsgType><![CDATA[text]]></MsgType>
                                  <Content><![CDATA[%s]]></Content>
                            </xml>''' % (openid, 'gh_93df1f1728b5', str(re.split('传统解卦', xiang_ci)[0]))
        elif content == '。':
            return_content = return_content % (openid, 'wubalubadubdub')
        else:
            return_content = return_content % (openid, 'I am Mr.meeseeks!!!')
        return return_content
    except:
        print(traceback.format_exc())


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
            print(data)
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
            user_id = request.form.get('user_id', '')
            create_time = datetime.datetime.now()
            sql = ''' insert into user_contents (user_id, content,create_time)values(%s,%s,%s)'''
            cursor.execute(sql, (user_id, content, create_time))
            conn.commit()
            return json.dumps({'ret': 0, 'msg': '成功'})
    except:
        print(traceback.format_exc())
    finally:
        conn.close()
