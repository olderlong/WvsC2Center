#! /usr/bin/env python
# _*_coding:utf-8 -*_

from flask import Flask
from config import web_server_config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(web_server_config[config_name])
    web_server_config[config_name].init_app(app)


    # 附加路由及默认错误处理页面
    # 主页面
    from .main import main as main_bp
    app.register_blueprint(main_bp)
    # 任务管理
    from .task import task as task_bp
    app.register_blueprint(task_bp, url_prefix='/task')


    return app

