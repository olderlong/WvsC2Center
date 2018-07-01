#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import time
import logging

logger = logging.getLogger("Server")


class AgentState(object):
    def __init__(self, name="AgentName", address=("127.0.0.1", 5000), timestamp=None, state="Online"):
        self.name = name
        self.address = address
        if timestamp is None:
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp
        self.state = state

        self.agent_identifier = "[{}:{}]".format(self.address[0], self.address[1])

    def gen_from_json_obj(self, json_state_obj):
        self.name = json_state_obj["Name"]
        self.address = json_state_obj["Address"]
        self.state = json_state_obj["State"]
        self.timestamp = json_state_obj["Timestamp"]
        self.agent_identifier = "[{}:{}]".format(self.address[0], self.address[1])

    def gen_json_object(self):
        res = {}
        res["Name"] = self.name
        res["Address"] = self.address
        res["Timestamp"] = self.timestamp
        res["State"] = self.state
        return res

    def update_state(self, timestamp, state):
        self.timestamp = timestamp
        self.state = state

    def print_state(self):
        logger.info("Agent {}{} is {} at {}".format(self.name, self.agent_identifier, self.state, self.timestamp))




