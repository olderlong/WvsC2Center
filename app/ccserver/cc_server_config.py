#! /usr/bin/env python
# _*_coding:utf-8 -*_

import os
import json
from config import basedir


class CCServerConfig(object):
    IP = "127.0.0.1"
    Port = 6000
    Protocol = "UDP"
    Address = (IP, Port)
    STATE_UPDATE_INTERVAL = 5
    ConfigJsonObj = {}

    @staticmethod
    def load_config():
        CCServerConfig.ConfigJsonObj = CCServerConfig.__get_ccserver_config()
        CCServerConfig.IP = CCServerConfig.ConfigJsonObj["ServerIP"]
        CCServerConfig.Port = CCServerConfig.ConfigJsonObj["ServerPort"]
        CCServerConfig.Protocol = CCServerConfig.ConfigJsonObj["Protocol"]
        CCServerConfig.STATE_UPDATE_INTERVAL = CCServerConfig.ConfigJsonObj["STATE_UPDATE_INTERVAL"]
        CCServerConfig.Address = (CCServerConfig.IP, CCServerConfig.Port)

    @staticmethod
    def save_config():
        config_file = os.path.join(basedir, "ccserver_config.json")
        with open(config_file, 'w', encoding='utf-8') as wf:
            json.dump(CCServerConfig.ConfigJsonObj, wf)

    @staticmethod
    def __get_ccserver_config():
        config_file = os.path.join(basedir, "ccserver_config.json")
        with open(config_file, 'r', encoding='utf-8') as rf:
            return json.load(rf)
