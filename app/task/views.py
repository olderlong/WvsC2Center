import time, logging
from flask import render_template, redirect, url_for,flash, request

from . import task
from .forms import NewScanTaskForm
from app.scan_session import *
from app.lib import MessageBus, CommonMsg

log = logging.getLogger("Server")


@task.route("/", methods=['GET', 'POST'])
def index():
    new_task_form = NewScanTaskForm()
    task_info_list, _ = ScanTaskManager().load_all_task_info()
    task_name = WvssState().get_current_scan_config()[0]

    if new_task_form.is_submitted():
        if not new_task_form.validate():
            task_name = new_task_form.Name.data
            start_url = new_task_form.StartURL.data
            scan_policy = new_task_form.ScanPolicy.data

            ScanTaskManager().new_task(task_name, start_url, scan_policy)
            task_info_list, _ = ScanTaskManager().load_all_task_info()
            # log.info("Task list is {}".format(task_info_list))

            # WvssState().set_current_scan_config(ScanSetting().get_scan_setting())

            if request.form.get("submit_new_and_start") == u"新建任务并运行":
                setting = ScanSetting()
                WvssState().set_current_scan_config(ScanSetting().get_scan_setting())
                start_scan_cmd = {
                    "Type": "WVSCommand",
                    "Data": {
                        "Action": "StartNewScan",
                        "Config": {  # 可选，当命令为StartNewScan时需提供该字段作为扫描参数
                            "StartURL": setting.start_url,
                            "ScanPolicy": setting.scan_policy
                        }
                    }
                }

                CommonMsg.msg_server_command.data = start_scan_cmd
                MessageBus.send_msg(CommonMsg.msg_server_command)

                GlobalVar.ScanState = "Started"
                log.info("Start scan....")
                return redirect(url_for("monitor.index"))

            # return render_template('task.html', title="扫描任务管理", NewTaskForm=new_task_form)
            return redirect(url_for('task.index'))
        else:
            flash('Invalid username or password.')

    return render_template('task.html',
                           title="扫描任务管理",
                           NewTaskForm=new_task_form,
                           task_info_list=task_info_list,
                           scan_state=GlobalVar.ScanState,
                           run_task_name=task_name
                           )


@task.route("/delete/<task_name>", methods=['GET', 'POST'])
def delete(task_name):
    if task_name:
        log.info("删除任务: {}".format(task_name))
        log.info("删除前任务: {}".format(ScanTaskManager().scan_task_list))
        ScanTaskManager().del_task(task_name)

        return redirect(url_for("task.index"))


@task.route("/result_info/<task_name>",methods=['GET', 'POST'])
def result_info(task_name):
    if task_name:
        _, scan_config, result_list = ScanTaskManager().load_task_info(task_name)
        WvssState().set_current_scan_config(scan_config)
        log.info(result_list)
        return redirect(url_for("result.index"))


@task.route("/start_scan/<task_name>", methods=['GET', 'POST'])
def start_scan(task_name):
    _, scan_setting, _ = ScanTaskManager().load_task_info(task_name)
    log.info(scan_setting)
    if scan_setting[1] is "":
        return redirect(url_for("task.index"))
    ScanTaskManager().save_task(task_name)

    start_scan_cmd = {
        "Type": "WVSCommand",
        "Data": {
            "Action": "StartNewScan",
            "Config": {  # 可选，当命令为StartNewScan时需提供该字段作为扫描参数
                "StartURL": scan_setting[1],
                "ScanPolicy": scan_setting[2]
            }
        }
    }
    WvssState().set_current_scan_config(ScanSetting().get_scan_setting())

    CommonMsg.msg_server_command.data = start_scan_cmd
    MessageBus.send_msg(CommonMsg.msg_server_command)

    GlobalVar.ScanState = "Started"
    log.info("Start scan....")

    return redirect(url_for("monitor.index"))


@task.route("/stop_scan", methods=['GET', 'POST'])
def stop_scan():
    stop_scan_cmd = {
        "Type": "WVSCommand",
        "Data": {
            "Action": "StopScan",
        }
    }
    WvssState().set_current_scan_config(None)
    CommonMsg.msg_server_command.data = stop_scan_cmd
    MessageBus.send_msg(CommonMsg.msg_server_command)

    GlobalVar.ScanState = "Stopped"
    log.info("Stopped scan")
    return redirect(url_for("monitor.index"))