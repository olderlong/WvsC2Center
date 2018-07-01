#! /usr/bin/env python3
# _*_coding:utf-8 -*_
from .message_bus import Message


class CommonMsg(object):
    MSG_HEARTBEAT = "Heartbeat"
    msg_heartbeat = Message(subject=MSG_HEARTBEAT)

    MSG_AGENT_STATE_UPDATE = "AgentStateUpdate"
    msg_agent_state_update = Message(subject=MSG_AGENT_STATE_UPDATE)

    MSG_WVS_STATE = "WVSState"
    msg_wvs_state = Message(subject=MSG_WVS_STATE)

    MSG_SCAN_RESULT_RECEIVE = "ScanResultReceive"
    msg_scan_result_receive = Message(subject=MSG_SCAN_RESULT_RECEIVE)

    MSG_WVS_COMMAND = "WVSCommand"
    msg_wvs_command = Message(subject=MSG_WVS_COMMAND)

    MSG_SERVER_COMMAND = "ServerCommand"
    msg_server_command = Message(subject=MSG_SERVER_COMMAND)

    MSG_AGENT_EXIT = "AgentExit"
    msg_agent_exit = Message(subject=MSG_AGENT_EXIT)