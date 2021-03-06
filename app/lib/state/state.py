#! /usr/bin/env python3
# _*_coding:utf-8 -*_

import time
import hashlib
import json


class State():
    """状态类
    """
    def __init__(self, name, type, address=("127.0.0.1", 6000)):
        """状态类初始化函数

        Args:
            name ([type]): 名称
            type ([type]): 类型
            address (tuple, optional): 代理地址. Defaults to ("127.0.0.1", 6000).
        """
        self.name = name
        self.type = type
        self.address = address
        self.state_code = ""
        self.state_detail = ""
        self.timestamp = time.time()

        self.identifier = self.__gen_identifier()

    def __gen_identifier(self):
        """生成id标识

        Returns:
            [type]: [description]
        """
        id_str = "{}_{}_{}".format(self.name, self.type, self.address)
        md5_obj = hashlib.md5()
        md5_obj.update(id_str.encode(encoding='utf-8'))
        return md5_obj.hexdigest().upper()

    def update_state(self, state_code, state_detail=""):
        """更新状态

        Args:
            state_code ([type]): 状态码
            state_detail (str, optional): 状态描述. Defaults to "".
        """
        self.state_code = state_code
        self.state_detail = state_detail
        self.timestamp = time.time()

    def get_json_obj(self):
        state_json_obj = {
            "Identifier": self.identifier,
            "Name": self.name,
            "Type": self.type,
            "Address": self.address,
            "Timestamp": self.timestamp,
            "StateCode": self.state_code,
            "StateDetail": self.state_detail
        }
        return state_json_obj

    def __str__(self):
        state_str = json.dumps(self.get_json_obj())
        return state_str

    def __eq__(self, other):
        if self.identifier == other.identifier and self.state_code == other.state_code and self.state_detail == other.state_detail:
            return True
        else:
            return False


if __name__ == '__main__':
    state = State("AppscanAgent", "WVSAgent")
    state.update_state("Online")
    print(state)