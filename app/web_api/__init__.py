# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)


from app.web_api import main_index
