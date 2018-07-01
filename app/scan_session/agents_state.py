#! /usr/bin/env python
# _*_coding:utf-8 -*_

import time
from config import singleton


@singleton
class AgentsState(object):
    def __init__(self):
        self.agent_list = []

    def has(self, state):
        identifier = "{}_{}".format(state["Name"], state["Address"][0])
        for i in range(len(self.agent_list)):
            wvs_identifier = "{}_{}".format(self.agent_list[i]["Name"], self.agent_list[i]["Address"][0])
            if wvs_identifier == identifier:
                return True, i

        return False, -1

    def add_agent_state(self, state):
        existed, index = self.has(state)
        state["Timestamp"] = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(state["Timestamp"]))
        if not existed:
            self.agent_list.append(state)
        else:
            self.agent_list[index] = state

    def get_agent_list(self):
        return self.agent_list

    def remove_agent(self, state):
        existed, index = self.has(state)
        if existed:
            self.agent_list.remove(state)