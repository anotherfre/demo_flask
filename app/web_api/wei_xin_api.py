# -*- coding: utf-8 -*-
from app.web_api import *
import random
from app.web_api.gua_data import *
import xmltodict
import requests


def get_str_sha1_secret_str(res):
    import hashlib
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(res.encode('utf-8'))
    encrypts = sha.hexdigest()
    return encrypts


# 微信公众号验证接口
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


# 微信公众号获取卦象接口
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
            url = "http://api.qingyunke.com/api.php?key=free&appid=0&msg={msg}"
            resp = requests.get(url.format(msg=content))
            answer = "学吧，太深奥了。"
            if resp.status_code == 200:
                decode_resp = json.loads(resp.text)
                answer = decode_resp.get('content')
            return_content = return_content % (openid, answer)
        return return_content
    except:
        print(traceback.format_exc())


# 微信小程序商品接口
@admin.route('/goods', methods=['GET'])
def goods():
    conn = get_connection()
    if not conn:
        return json.dumps({'ret': -1, 'status': 'failed'})
    try:
        with conn.cursor() as cursor:
            page = 1
            sql = ''' select id, goods_name, goods_pic, goods_price from goods order by create_time desc'''
            sql += ' limit {page}, {limit}'.format(page=(int(page) - 1) * 10, limit=10)
            result = []
            if cursor.execute(sql):
                query_data = cursor.fetchall()
            else:
                return json.dumps({"ret": -2, "data": []})

            for query in query_data:
                result.append({'id': query.get('id'),
                               'goods_name': query.get('goods_name'),
                               'goods_pic': query.get('goods_pic'),
                               'goods_price': query.get('goods_price')})
            data = {
                "ret": 0,
                "data": result
            }
            return json.dumps(data)

    except Exception as e:
        return json.dumps({'ret': -3, 'status': 'failed'})


# 微信用户登录信息
@admin.route('/users', methods=['POST', 'GET'])
def users():
    conn = get_connection()
    if not conn:
        return json.dumps({'ret': -1, 'status': 'failed'})
    try:
        with conn.cursor() as cursor:
            sql = """select id, user_name, user_icon from wx_users limit 1"""
            result = []
            if cursor.execute(sql):
                query_data = cursor.fetchone()
                result.append(query_data)

            data = {
                "ret": 0,
                "data": result
            }
            return json.dumps(data)
    except Exception as e:
        return json.dumps({'ret': -3, 'status': 'failed'})


if __name__ == '__main__':
    app_id = 'wx2cfa87927a21509c'
    app_secret = 'ba904cc98a437dd7a7ada60dcd3036cd'
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
    resp = requests.get(url.format(APPID=app_id, APPSECRET=app_secret))

    access_token = json.loads(resp.text).get('access_token')
    create_api_url = ' https://api.weixin.qq.com/cgi-bin/menu/create?access_token={ACCESS_TOKEN}'
    data = {
        "button": [
            {"type": "view",
             "name": "今日红包",
             "url": ""}
        ]
    }
    resp = requests.post(create_api_url.format(ACCESS_TOKEN=access_token), data=data)
    pass
