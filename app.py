# -*- coding: utf-8 -*-
from flask import Flask, render_template
import os
from web_api import admin as admin_blueprint


app = Flask(__name__)


app.register_blueprint(admin_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
