# -*- coding: utf-8 -*-
import re
from flask import Blueprint, render_template, request, session
import json
import pymysql
import traceback
from dbutils.pooled_db import PooledDB, SharedDBConnection
import datetime

admin = Blueprint('admin', __name__)

conn_pool = PooledDB(
    creator=pymysql,
    maxconnections=100,
    mincached=3,
    maxcached=6,
    blocking=True,
    maxusage=None,
    ping=0,
    host='192.168.184.129',
    user='root',
    password='123456789cJ.',
    db='demo_database',
    port=3306,
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


def get_connection():
    try:
        get_conn = conn_pool.connection()
        return get_conn
    except:
        return False


from web_api import wei_xin_api
from web_api import celery_task, main_index, user_content


def get_str_sha1_secret_str(res):
    import hashlib
    """
    使用sha1加密算法，返回str加密后的字符串
    """
    sha = hashlib.sha1(res.encode('utf-8'))
    encrypts = sha.hexdigest()
    return encrypts
