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
            return_content = return_content % (openid, 'I am Mr.meeseeks!!!')
        return return_content
    except:
        print(traceback.format_exc())
