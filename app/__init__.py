#! /usr/bin/env python
# _*_coding:utf-8 -*_
from flask_socketio import SocketIO
from flask import Flask, session
from config import web_server_config
from app.ccserver import CliApp
from app.scan_session import GlobalVar


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(web_server_config[config_name])
    web_server_config[config_name].init_app(app)

    # socketio赋给全局变量GlobalVar.SocketIO
    async_mode = None
    GlobalVar.SocketIO = SocketIO(app, async_mode=async_mode)

    # 附加路由及默认错误处理页面
    # 主页面
    from .main import main as main_bp
    app.register_blueprint(main_bp)

    # 扫描任务管理蓝图
    from .task import task as task_bp
    app.register_blueprint(task_bp, url_prefix='/task')

    # 扫描监控蓝图
    from .monitor import monitor as monitor_bp
    app.register_blueprint(monitor_bp, url_prefix='/monitor')

    # 扫描结果处理蓝图
    from .result import result as result_bp
    app.register_blueprint(result_bp, url_prefix='/result')

    # 运行CC服务器
    CliApp().run()

    from app.lib import MessageBus, CommonMsg
    import app.result.views as result_view
    MessageBus.add_msg_listener(CommonMsg.MSG_SCAN_RESULT_RECEIVE, result_view.scan_result_handler)
    import app.monitor.views as monitor_view
    MessageBus.add_msg_listener(CommonMsg.MSG_WVS_STATE, monitor_view.ws_wvs_state_send)
    MessageBus.add_msg_listener(CommonMsg.MSG_AGENT_STATE_UPDATE, monitor_view.ws_agent_state_send)


    return app

