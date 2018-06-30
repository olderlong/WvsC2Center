# _*_coding:utf-8 -*_
import time
from config import singleton

class TaskInfo(object):
    def __init__(self, task_info_dict=None):
        if task_info_dict:
            self.task_info_dict = task_info_dict
            self.start_url = self.task_info_dict["ScanSetting"]["StartURL"]
            self.scan_policy = self.task_info_dict["ScanSetting"]["ScanPolicy"]
            self.scan_result_file = self.task_info_dict["ScanResultFile"]
            self.timestamp = self.task_info_dict["Timestamp"]
        else:
            self.task_info_dict = {}
            self.start_url = ""
            self.scan_policy = ""
            self.scan_result_file = "scan_result.json"
            self.timestamp = time.time()
            self.task_info_dict["ScanSetting"] = {}
            self.task_info_dict["ScanSetting"]["StartURL"] = self.start_url
            self.task_info_dict["ScanSetting"]["ScanPolicy"] = self.scan_policy
            self.task_info_dict["ScanResultFile"] = self.scan_result_file
            self.task_info_dict["Timestamp"] = self.timestamp

    def get_task_info_dict(self):
        self.task_info_dict["ScanSetting"] = {}
        self.task_info_dict["ScanSetting"]["StartURL"] = self.start_url
        self.task_info_dict["ScanSetting"]["ScanPolicy"] = self.scan_policy
        self.task_info_dict["ScanResultFile"] = self.scan_result_file
        self.task_info_dict["Timestamp"] = self.timestamp
        return self.task_info_dict