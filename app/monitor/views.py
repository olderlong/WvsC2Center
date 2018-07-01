import logging
from flask import render_template, redirect, url_for, request

from . import monitor
from .forms import ScanControlForm

from app.lib import MessageBus, CommonMsg
from app.ccserver import CCServerConfig
from app.scan_session import ScanSetting, AgentsState, WvssState, GlobalVar


logger = logging.getLogger("Server")


@monitor.route("/", methods=["GET", "POST"])
def index():
    scan_control_form = ScanControlForm()

    if scan_control_form.is_submitted():
        task_name, start_url, scan_policy = ScanSetting().get_scan_setting()
        if task_name is "" or start_url is "":
            return redirect(url_for("monitor.index"))

        if request.form.get("submit_start_scan") == u"开始扫描":
            start_scan_cmd = {
                    "Type": "WVSCommand",
                    "Data": {
                        "Action": "StartNewScan",
                        "Config": {  # 可选，当命令为StartNewScan时需提供该字段作为扫描参数
                            "StartURL": start_url,
                            "ScanPolicy": scan_policy
                        }
                    }
            }

            CommonMsg.msg_server_command.data = start_scan_cmd
            MessageBus.send_msg(CommonMsg.msg_server_command)

            WvssState().set_current_scan_config(ScanSetting().get_scan_setting())
            GlobalVar.ScanState = "Started"
            logger.info("Start scan....")

            return redirect(url_for("monitor.index"))
        elif request.form.get("submit_stop_scan") == u"停止扫描":
            stop_scan_cmd = {
                "Type": "WVSCommand",
                "Data": {
                    "Action": "StopScan",
                }
            }

            CommonMsg.msg_server_command.data = stop_scan_cmd
            MessageBus.send_msg(CommonMsg.msg_server_command)
            WvssState().set_current_scan_config(None)
            GlobalVar.ScanState = "Stopped"
            logger.info("Stopped scan")
            return redirect(url_for("monitor.index"))
        else:
            pass

    return render_template(
        "monitor.html",
        title="监控中心",
        server_config=CCServerConfig(),
        scan_config=WvssState().get_current_scan_config(),
        agent_state_list=AgentsState().get_agent_list(),
        wvs_state_list=WvssState().get_wvs_state_list(),
        scan_state=GlobalVar.ScanState,
        scan_control_form=scan_control_form
    )


@GlobalVar.SocketIO.on("connect", namespace="/agent_state_ns")
def ws_agent_state_connect():
    MessageBus.add_msg_listener(CommonMsg.MSG_AGENT_STATE_UPDATE, ws_agent_state_send)
    logger.info("Agent state websocket is connected")


def ws_agent_state_send(msg):
    agent_state = msg.data
    AgentsState().add_agent_state(agent_state)
    GlobalVar.SocketIO.emit(
        "agent_state_update",
        agent_state,
        namespace="/agent_state_ns"
    )
    logger.info("Send agent state: {}".format(agent_state))


@GlobalVar.SocketIO.on("connect", namespace="/wvs_state_ns")
def ws_wvs_state_connect():
    MessageBus.add_msg_listener(CommonMsg.MSG_WVS_STATE, ws_wvs_state_send)
    logger.info("Wvs state websocket is connected")


def ws_wvs_state_send(msg):
    wvs_state = msg.data
    WvssState().add_wvs_state(wvs_state)
    GlobalVar.SocketIO.emit(
        "wvs_state_update",
        wvs_state,
        namespace="/wvs_state_ns"
    )
    logger.info("Send wvs state: {}".format(wvs_state))
