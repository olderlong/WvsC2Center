#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask_wtf import FlaskForm
from wtforms import SubmitField


class ScanControlForm(FlaskForm):
    submit_start_scan = SubmitField('开始扫描')
    submit_stop_scan = SubmitField('停止扫描')