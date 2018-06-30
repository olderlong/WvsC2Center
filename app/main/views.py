#! /usr/bin/env python
# _*_coding:utf-8 -*_
import time
from flask import render_template, session, redirect, url_for

from . import main


@main.route("/", methods=['GET', 'POST'])
def index():
    # return redirect(url_for('main.index'))
    return render_template('index.html')
