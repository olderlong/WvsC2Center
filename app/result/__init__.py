#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask import Blueprint

result = Blueprint("result", __name__)

from . import views, errors
