#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import time
import logging

logger = logging.getLogger("Server")


class AgentState(object):
    """代理状态类

    Args:
        object ([type]): [description]
    """
    def __init__(self,
                 name="AgentName",
                 address=("127.0.0.1", 5000),
                 timestamp=None,
                 state="Online"):
        """初始化

        Args:
            name (str, optional): [description]. Defaults to "AgentName".
            address (tuple, optional): [description]. Defaults to ("127.0.0.1", 5000).
            timestamp ([type], optional): [description]. Defaults to None.
            state (str, optional): [description]. Defaults to "Online".
        """
        self.name = name
        self.address = address
        if timestamp is None:
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp
        self.state = state

        self.agent_identifier = "[{}:{}]".format(self.address[0],
                                                 self.address[1])

    def gen_from_json_obj(self, json_state_obj):
        """从状态的json对象中生成数据

        Args:
            json_state_obj ([type]): [description]
        """
        self.name = json_state_obj["Name"]
        self.address = json_state_obj["Address"]
        self.state = json_state_obj["State"]
        self.timestamp = json_state_obj["Timestamp"]
        self.agent_identifier = "[{}:{}]".format(self.address[0],
                                                 self.address[1])

    def gen_json_object(self):
        """生成json对象

        Returns:
            [type]: [description]
        """
        res = {}
        res["Name"] = self.name
        res["Address"] = self.address
        res["Timestamp"] = self.timestamp
        res["State"] = self.state
        return res

    def update_state(self, timestamp, state):
        """更新状态

        Args:
            timestamp ([type]): 状态时间戳
            state ([type]): 更新的状态
        """
        self.timestamp = timestamp
        self.state = state

    def print_state(self):
        """打印状态
        """
        logger.info("Agent {}{} is {} at {}".format(self.name,
                                                    self.agent_identifier,
                                                    self.state,
                                                    self.timestamp))
