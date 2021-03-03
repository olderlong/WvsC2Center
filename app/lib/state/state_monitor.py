#! /usr/bin/env python3
# _*_coding:utf-8 -*_

import time
import threading
import copy


class StateMonitor(object):
    """状态监视类

    Args:
        object ([type]): [description]
    """
    def __init__(self, name=None):
        if name:
            self.name = name
        else:
            self.name = "StateMonitor"

        self.expire_time = 30.0
        self.__running = threading.Event()
        self.__state_monitor_thread = threading.Thread(
            target=self.__state_monitor)

        self.all_state_dict = {}

    def __state_monitor(self):
        while self.__running:
            if len(self.all_state_dict) > 0:
                for state in list(self.all_state_dict.values()):
                    if time.time() - state.timestamp > self.expire_time:
                        state.update_state("offline")
                        self.all_state_dict[state.identifier] = state
                        print("{} is offline :: {}".format(
                            state.identifier, state))
                time.sleep(1)

    def start_monitor(self, expire_time=30.0):
        self.expire_time = expire_time
        self.__running.set()
        if self.__state_monitor_thread.is_alive():
            pass
        else:
            self.__state_monitor_thread.daemon = True
            self.__state_monitor_thread.start()

    def stop_monitor(self):
        self.__running.clear()
        self.all_state_dict.clear()

    def add_state(self, state):
        if state.identifier in self.all_state_dict.keys():
            old_sate = self.all_state_dict[state.identifier]
            if old_sate == state:
                print("State {} is not changed".format(state.identifier))
            else:
                print("State {} is changed".format(state.identifier))
        else:
            print("Add new state: {}".format(state))
        # 这里使用深copy， 否则old state 和state是同一个对象，无法判断是否变化
        self.all_state_dict[state.identifier] = copy.deepcopy(state)

    def get_state_list(self):
        return list(self.all_state_dict.values())

    def __str__(self):
        state_list_str = "The state list of {} is: \n".format(self.name)
        if len(self.all_state_dict) > 0:
            for state in list(self.all_state_dict.values()):
                state_list_str = state_list_str + "{}\n".format(state)

        return state_list_str
