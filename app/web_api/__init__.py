# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
import json
import pymysql
import traceback
from dbutils.pooled_db import PooledDB, SharedDBConnection

admin = Blueprint('admin', __name__)

conn_pool = PooledDB(
    creator=pymysql,
    maxconnections=100,
    mincached=3,
    maxcached=6,
    blocking=True,
    maxusage=None,
    ping=0,
    host='39.97.106.192',
    user='root',
    password='123456',
    db='remote_databases',
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


from app.web_api import main_index
