#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import threading
import time
import logging

from app.lib import MessageBus, CommonMsg
from config import singleton

from .cc_server_config import CCServerConfig
from .agent_state import AgentState

logger = logging.getLogger("Server")


@singleton
class AgentStateMonitor(object):
    """
    代理状态监视类，为单例模式
    """
    def __init__(self):
        self.agent_state_dict = dict()
        self.__running = threading.Event()
        self.__state_monitor_thread = threading.Thread(
            target=self.__agents_state_monitor)
        MessageBus.add_msg_listener(CommonMsg.MSG_HEARTBEAT,
                                    self.add_new_agent_state)

    def add_new_agent_state(self, msg):
        """添加新的代理状态

        Args:
            msg (Message): [description]
        """
        state_data = msg.data
        agent_state = AgentState()
        agent_state.gen_from_json_obj(state_data)
        agent_state.timestamp = time.time()
        # self.update_agent_state(agent_state)
        self.agent_state_dict[agent_state.agent_identifier] = agent_state

    def update_agent_state(self, agent_state):
        """更新代理状态

        Args:
            agent_state ([type]): 代理状态
        """
        self.agent_state_dict[agent_state.agent_identifier] = agent_state
        agent_state.print_state()

    def start_monitor(self):
        self.__running.set()
        if self.__state_monitor_thread.is_alive():
            pass
        else:
            self.__state_monitor_thread.daemon = True
            logger.info("Agent state monitor thread is running...")
            self.__state_monitor_thread.start()

    def stop_monitor(self):
        self.__running.clear()
        self.agent_state_dict.clear()

    def __agents_state_monitor(self):
        while self.__running:
            if len(self.agent_state_dict) > 0:
                for agent_state in list(self.agent_state_dict.values()):
                    new_state = self.__check_state(agent_state)
                    if new_state == "Dead":
                        logger.info(
                            "Agent {0} is dead.\nAgent {1} is removed.".format(
                                agent_state.agent_identifier,
                                agent_state.agent_identifier))

                        agent_state.state = new_state
                        CommonMsg.msg_agent_state_update.data = agent_state.gen_json_object(
                        )
                        MessageBus.send_msg(CommonMsg.msg_agent_state_update)

                        self.agent_state_dict.pop(agent_state.agent_identifier)
                    else:
                        agent_state.state = new_state
                        self.agent_state_dict[
                            agent_state.agent_identifier] = agent_state

                        CommonMsg.msg_agent_state_update.data = agent_state.gen_json_object(
                        )
                        MessageBus.send_msg(CommonMsg.msg_agent_state_update)

                        time.sleep(1)

            time.sleep(CCServerConfig.STATE_UPDATE_INTERVAL)

    def __check_state(self, agent_state):
        """
        根据前后两次时标对比判断代理状态，时标间隔大于2倍更新时间小于3倍更新时间时为离线，更长时间为Dead
        :param agent_state: 代理状态对象
        :return: 代理状态：Offline、Dead、Online
        """
        last_time = time.time() - agent_state.timestamp
        if CCServerConfig.STATE_UPDATE_INTERVAL * 2.0 < last_time <= CCServerConfig.STATE_UPDATE_INTERVAL * 5.0:
            return "Offline"
        elif last_time > CCServerConfig.STATE_UPDATE_INTERVAL * 5.0:
            return "Dead"
        else:
            return "Online"


if __name__ == '__main__':
    monitor = AgentStateMonitor()
    print(id(monitor))

    monitor.start_monitor()

    CommonMsg.msg_heartbeat.data = {
        "Name": "tste",
        "Address": ("127.0.0.1", 5555),
        "Timestamp": time.time(),
        "State": "Online"
    }
    MessageBus().send_msg(CommonMsg.msg_heartbeat)
    time.sleep(20)
