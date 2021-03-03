#! /usr/bin/env python3
# _*_coding:utf-8 -*_
from .message_bus import Message


class CommonMsg(object):
    """[summary]

    Args:
        object ([type]): [description]
    """
    # 心跳消息
    MSG_HEARTBEAT = "Heartbeat"
    msg_heartbeat = Message(subject=MSG_HEARTBEAT)

    # 代理状态更新消息
    MSG_AGENT_STATE_UPDATE = "AgentStateUpdate"
    msg_agent_state_update = Message(subject=MSG_AGENT_STATE_UPDATE)

    # 代理状态消息
    MSG_WVS_STATE = "WVSState"
    msg_wvs_state = Message(subject=MSG_WVS_STATE)

    # 扫描结果接收消息
    MSG_SCAN_RESULT_RECEIVE = "ScanResultReceive"
    msg_scan_result_receive = Message(subject=MSG_SCAN_RESULT_RECEIVE)

    # wvs命令消息
    MSG_WVS_COMMAND = "WVSCommand"
    msg_wvs_command = Message(subject=MSG_WVS_COMMAND)

    # 服务器命令
    MSG_SERVER_COMMAND = "ServerCommand"
    msg_server_command = Message(subject=MSG_SERVER_COMMAND)

    # 代理退出
    MSG_AGENT_EXIT = "AgentExit"
    msg_agent_exit = Message(subject=MSG_AGENT_EXIT)