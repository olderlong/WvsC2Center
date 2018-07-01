#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask import Blueprint

monitor = Blueprint("monitor", __name__)

from . import views, errors
