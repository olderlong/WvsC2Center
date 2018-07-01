#! /usr/bin/env python
# _*_coding:utf-8 -*_

import time
from config import singleton
from .scan_setting import ScanSetting


@singleton
class WvssState:
    def __init__(self):
        self.wvs_state_list = []
        self.current_scan_config = ("", "", "Normal")

    def has(self, state):
        identifier = "{}_{}".format(state["Name"], state["Address"][0])
        for i in range(len(self.wvs_state_list)):
            wvs_identifier = "{}_{}".format(self.wvs_state_list[i]["Name"], self.wvs_state_list[i]["Address"][0])
            if wvs_identifier == identifier:
                return True, i

        return False, -1

    def add_wvs_state(self, state):
        existed, index = self.has(state)
        if not existed:
            state["Timestamp"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(state["Timestamp"]))
            self.wvs_state_list.append(state)
        else:
            state["Timestamp"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(state["Timestamp"]))
            self.wvs_state_list[index] = state

    def get_wvs_state_list(self):
        return self.wvs_state_list

    def remove_agent(self, state):
        existed, index = self.has(state)
        if existed:
            self.wvs_state_list.remove(state)

    def set_current_scan_config(self, config):
        if config:
            self.current_scan_config = config
        else:
            self.current_scan_config = ("", "", "Normal")

    def get_current_scan_config(self):
        return self.current_scan_config