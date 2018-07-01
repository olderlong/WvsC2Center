import time, logging
from flask import render_template, redirect, url_for,flash

from . import result
from app.scan_session import *

logger = logging.getLogger("Server")


@result.route("/", methods=['GET', 'POST'])
def index():
    return render_template("result.html", title="扫描结果", scan_result_list=ScanResult().wvs_result_list)


@result.route("/report/<time>",methods=['GET', 'POST'])
def report(time):
    pass


@result.route("/save", methods=['GET', 'POST'])
def save():
    task_name = WvssState().get_current_scan_config()[0]
    logger.info("保存任务{}".format(task_name))
    # stm.add_new_task(ScanSetting().scan_name)
    ScanTaskManager().save_task(task_name)

    logger.info("任务列表：{}".format(ScanTaskManager().scan_task_list))

    return render_template("result.html", title="扫描结果", scan_result_list=ScanResult().wvs_result_list)


def scan_result_handler(msg):
    scan_res = msg.data
    ScanResult().add_scan_result(scan_res)
    existed = ScanResult().has(scan_res)
    if not existed:
        logger.info("Recive result data:\t{}".format(scan_res))
    GlobalVar.SocketIO.emit(
            "wvs_result_update",
            scan_res,
            namespace="/wvs_result"
        )
    logger.info("Send agent state: {}".format(scan_res))


@GlobalVar.SocketIO.on("connect", namespace="/wvs_result")
def wvs_result_connect():
    logger.info("Wvs result websocket is connected")