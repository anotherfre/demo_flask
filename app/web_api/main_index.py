# -*- coding: utf-8 -*-
from app.web_api import *


@admin.route('/')
def index():
    print(1)
    return render_template('index.html')




