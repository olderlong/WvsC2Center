#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask import Blueprint

task = Blueprint("task", __name__)

from . import views, errors
