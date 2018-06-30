import time
from flask import render_template, redirect, url_for,flash

from . import task
from .forms import NewScanTaskForm
from app.scan_session import *

@task.route("/", methods=['GET', 'POST'])
def index():
    new_task_form = NewScanTaskForm()
    task_info_list = ScanTaskManager().load_all_task_info()

    if new_task_form.is_submitted():
        if new_task_form.validate():
            task_name = new_task_form.Name.data
            start_url = new_task_form.StartURL.data
            scan_policy = new_task_form.ScanPolicy.data

            ScanTaskManager().new_task(task_name, start_url, scan_policy)
            task_info_list, _ = ScanTaskManager().load_all_task_info()
            # return render_template('task.html', title="扫描任务管理", NewTaskForm=new_task_form)
            return redirect(url_for('task.index'))
        else:
            flash('Invalid username or password.')

    return render_template('task.html', title="扫描任务管理", NewTaskForm=new_task_form, task_info_list=task_info_list)
