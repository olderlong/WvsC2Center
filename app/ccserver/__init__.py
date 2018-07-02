#! /usr/bin/env python
# _*_coding:utf-8 -*_
import logging

from config import singleton

from .cc_server import CCServer
from .agent_state import AgentState
from .agent_state_manager import AgentStateMonitor
from .cc_server_config import CCServerConfig

from app.lib import MessageBus


logger = logging.getLogger("Server")


@singleton
class CliApp(object):
    def __init__(self):
        CCServerConfig.load_config()
        self.__is_running = False
        self.server_ip = CCServerConfig.IP
        self.server_port = CCServerConfig.Port
        self.server = CCServer(ip=self.server_ip, port=self.server_port)
        self.agent_state_manager = AgentStateMonitor()

    def run(self):
        if self.__is_running:
            pass
        else:
            self.__is_running = True
            logger.info("CCServer is running <{}>...".format(CCServerConfig.Address))

            MessageBus.start()
            self.server.start()
            self.agent_state_manager.start_monitor()

    def stop(self):
        self.__is_running = False
        self.server.stop()
        self.agent_state_manager.stop_monitor()
        MessageBus.stop()
        CCServerConfig.save_config()

    def is_running(self):
        return self.__is_running


__all__ = ["CCServerConfig", "CCServer", "AgentStateMonitor", "AgentState", "CliApp"]