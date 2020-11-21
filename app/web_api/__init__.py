# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
import json

admin = Blueprint('admin', __name__)


from app.web_api import main_index
