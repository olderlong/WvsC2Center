#! /usr/bin/env python3
# _*_coding:utf-8 -*_
import json, os, time, shutil, zipfile, logging
from flask import render_template, session
from app.scan_session import ScanResult, WvssState

logger = logging.getLogger("Server")


class GenReport:
    """
    生成报告类
    """
    def __init__(self):

        self.scan_config = WvssState().get_current_scan_config()
        self.result_list = ScanResult().get_scan_result()
        # if session["TaskName"]:
        #     self.task_name = session["TaskName"]
        # else:
        #     self.task_name = ""
        self.task_name = "Task"
        self.report_path = os.path.join(os.getcwd(), "report_file")

    def __gen_html_report(self):
        report_file_name = time.strftime("Report_%Y_%m_%d_%H_%M_%S_",
                                         time.localtime(
                                             time.time())) + self.task_name
        self.del_files()
        html = render_template("report.html",
                               scan_config=self.scan_config,
                               scan_result_list=self.result_list)
        with open(os.path.join(self.report_path, "report.html"),
                  'w',
                  encoding="utf-8") as wf:
            wf.write(html)
        shutil.make_archive(os.path.join(self.report_path, report_file_name),
                            'zip', self.report_path)
        self.report_file_name = report_file_name + ".zip"

    def gen_report(self, filetype="html"):
        self.__gen_html_report()

    def del_files(self):
        for root, dirs, files in os.walk(self.report_path):
            for name in files:
                if name.endswith(".zip") or name.endswith(".html"):
                    os.remove(os.path.join(root, name))
                    logger.info("Remove file:{}".format(
                        os.path.join(root, name)))


if __name__ == '__main__':
    r = GenReport()
    print(r.report_file_name)