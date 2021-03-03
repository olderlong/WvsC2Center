#! /usr/bin/env python
# _*_coding:utf-8 -*_

import os
import json
from config import basedir


class CCServerConfig(object):
    """控制服务器配置类

    Args:
        object ([type]): [description]

    Returns:
        [type]: [description]
    """
    IP = "127.0.0.1"
    Port = 6000
    Protocol = "UDP"
    Address = (IP, Port)
    STATE_UPDATE_INTERVAL = 5
    ConfigJsonObj = {}

    @staticmethod
    def load_config():
        """
        从json对象中载入配置信息
        """
        CCServerConfig.ConfigJsonObj = CCServerConfig.__get_ccserver_config()
        CCServerConfig.IP = CCServerConfig.ConfigJsonObj["ServerIP"]
        CCServerConfig.Port = CCServerConfig.ConfigJsonObj["ServerPort"]
        CCServerConfig.Protocol = CCServerConfig.ConfigJsonObj["Protocol"]
        CCServerConfig.STATE_UPDATE_INTERVAL = CCServerConfig.ConfigJsonObj[
            "STATE_UPDATE_INTERVAL"]
        CCServerConfig.Address = (CCServerConfig.IP, CCServerConfig.Port)

    @staticmethod
    def save_config():
        """
        保存配置信息到文件
        """
        config_file = os.path.join(basedir, "ccserver_config.json")
        with open(config_file, 'w', encoding='utf-8') as wf:
            json.dump(CCServerConfig.ConfigJsonObj, wf)

    @staticmethod
    def __get_ccserver_config():
        """从配置文件中载入配置json对象

        Returns:
            [type]: 配置信息的json对象
        """
        config_file = os.path.join(basedir, "ccserver_config.json")
        with open(config_file, 'r', encoding='utf-8') as rf:
            return json.load(rf)
