#! /usr/bin/env python
# _*_coding:utf-8 -*_

from config import basedir, singleton


@singleton
class ScanSetting:
    """扫描设置类
    """
    def __init__(self, name=None, url="", policy="Normal"):
        self.start_url = url
        self.scan_policy = policy
        self.scan_name = name if name else "TaskName"

    def get_scan_setting(self):
        return self.scan_name, self.start_url, self.scan_policy

    def get_scan_setting_json(self):
        return {"StartURL": self.start_url, "ScanPolicy": self.scan_policy}

    def set_scan_setting(self, name="ScanName", url="", policy="Normal"):
        self.start_url = url
        self.scan_policy = policy
        self.scan_name = name