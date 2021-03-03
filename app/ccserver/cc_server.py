#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import json, logging
from app.lib import UDPEndPoint, MessageBus, CommonMsg

from .agent_state_manager import AgentStateMonitor

logger = logging.getLogger("Server")


class CCServer(UDPEndPoint):
    """控制服务器类

    Args:
        UDPEndPoint ([type]): 控制服务器类的基类，为UDP终端类
    """
    def __init__(self, ip=None, port=6000):
        """类的初始化

        Args:
            ip (str, optional): 服务器IP. Defaults to None.
            port (int, optional): 服务器端口. Defaults to 6000.
        """
        self.server_ip = ip
        self.port = port
        self.agent_list = []
        self.agent_state_monitor = AgentStateMonitor()

        MessageBus.add_msg_listener(CommonMsg.MSG_SERVER_COMMAND,
                                    self.send_command)
        super(CCServer, self).__init__(ip=self.server_ip,
                                       port=self.port,
                                       handler=self.receive_data_handler)

    def receive_data_handler(self, data, address):
        """接收数据处理函数

        Args:
            data ([type]): 接收的数据
            address ([type]): 接收数据的IP地址
        """
        if address not in self.agent_list:
            self.agent_list.append(address)

        pkg_obj = dict(json.loads(str(data, encoding='utf-8')))
        try:
            if pkg_obj["Type"] == "Heartbeat":  #心跳包
                CommonMsg.msg_heartbeat.data = pkg_obj["Data"]
                MessageBus.send_msg(CommonMsg.msg_heartbeat)
                # logger.info(CommonMsg.msg_heartbeat.data)

            elif pkg_obj["Type"] == "WVSState":
                CommonMsg.msg_wvs_state.data = pkg_obj["Data"]
                MessageBus.send_msg(CommonMsg.msg_wvs_state)
                logger.info(CommonMsg.msg_wvs_state.data)
                # print("收到代理{}的漏扫状态数据".format(address))

            elif pkg_obj["Type"] == "ScanResult":
                CommonMsg.msg_scan_result_receive.data = pkg_obj["Data"]
                MessageBus.send_msg(CommonMsg.msg_scan_result_receive)
                self.__print_scan_result(pkg_obj["Data"])
            else:
                print("收到来自{}的未知类型数据".format(address))
        except KeyError as e:
            print("收到来自{}的未知类型数据——{}".format(address, data))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def __print_scan_result(self, vul_result):
        """打印扫描结果

        Args:
            vul_result ([type]): 漏洞结果
        """
        result_str = "漏洞类型:\t{}\n漏洞URL:\t{}\n漏洞等级:\t{}\n漏洞信息:\t".format(
            vul_result["VulType"], vul_result["VulUrl"],
            vul_result["VulSeverity"])
        print(result_str)
        for info in vul_result["VulDetails"]:
            result_str = "\tURL参数变异:\t{}\n\t漏洞原因:\t{}\n\tCWE:\t{}\n\tCVE:\t{}".format(
                info["url_param_variant"], info["vul_reasoning"], info["CWE"],
                info["CVE"])
            print(result_str)
        print("\r\n")


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def send_command(self, msg):
        """发送命令

        Args:
            msg (dict): 命令信息，为dict对象
        """
        command_json = msg.data
        logger.info("in CCServer " + str(command_json))
        # print(self.agent_list)
        for address in self.agent_list:
            identifier = "[{}:{}]".format(address[0], address[1])
            if identifier in list(
                    self.agent_state_monitor.agent_state_dict.keys()):
                self.send_json_to(command_json, address)

    def send_config(self, msg):
        """发送配置信息

        Args:
            msg ([type]): 配置信息
        """
        config_json = msg.data
        for address in self.agent_list:
            identifier = "[{}:{}]".format(address[0], address[1])
            if identifier in list(
                    self.agent_state_monitor.agent_state_dict.keys()):
                self.send_json_to(config_json, address)

if __name__ == '__main__':
    server = CCServer()
    server.start()
    server.stop()