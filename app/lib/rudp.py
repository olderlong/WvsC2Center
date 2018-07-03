#! /usr/bin/env python3
# _*_coding:utf-8 -*_
import socket
import time
import threading
import json
import logging
import sys
from hashlib import md5


def init_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(pathname)s [line:%(lineno)d] %(levelname)s >>> %(message)s')

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # 为logger添加的日志处理器
    logger.addHandler(console_handler)
    return logger


logger = init_logger("RUDP")


class RUDP(object):
    def __init__(self, ip="127.0.0.1", port=4444, callback=None):
        self.ip = ip
        self.port = port
        self.address = (self.ip, self.port)
        self.udp_socket = None
        self.buff_size = 4096

        self.recvieve_data_handler = callback
        self.__recvieve_thread = threading.Thread(target=self.__recvieve)
        self.__running = threading.Event()  # 用于停止线程的标识

        self.__heartbeat_thread = threading.Thread(target=self.__heartbeat)

        self.__remote_socket_list = []

    def start(self):
        if self.__init_socket():
            self.__running.set()

            self.__recvieve_thread.daemon = True
            self.__recvieve_thread.start()

            self.__heartbeat_thread.daemon = True
            self.__heartbeat_thread.start()

    def stop(self):
        self.__running.clear()

    def __send_data_to(self,data, datatype, address):
        if self.udp_socket.fileno() > 0:
            send_data_obj = self.__pack_data(data, datatype)
            send_data_str = json.dumps(send_data_obj)
            self.udp_socket.sendto(bytes(send_data_str, "utf-8"), address)

    def send_data_to_all(self):
        pass

    def send_msg_to(self,str_msg, datatype, address):
        self.__send_data_to(bytes(str_msg, "utf-8"),datatype, address)

    def send_obj_to(self, json_obj, datatype, address):
        json_str = json.dumps(json_obj)
        self.__send_data_to(bytes(json_str, "utf-8"), datatype, address)

    def __init_socket(self):
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.bind(self.address)
            self.address = self.udp_socket.getsockname()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def __recvieve(self):
        while self.__running:
            logger.info("In recieve thread")
            try:
                data, address = self.udp_socket.recvfrom(self.buff_size)
                self.__remote_socket_list.append(address)

                data_type, raw_data_str, signature, timestramp = self.__unpack_data(data)

                if data_type == "Data":
                    raw_data = bytes(raw_data_str, "utf-8")
                    logger.info("接收{}发送的{}类型数据,数据签名：{}，时间戳：{}".format(address, data_type, signature, timestramp))
                    ack_data = {"Type": "Ack", "Data": "Ack of {}".format(signature), "Signature": signature,
                                "Timestramp": time.time()}
                    ack_data_str = json.dumps(ack_data)
                    self.udp_socket.sendto(bytes(ack_data_str,"utf-8"), address)
                    threading.Thread(target=self.recvieve_data_handler, args=(raw_data, address,)).start()

                elif data_type == "Ack":
                    logger.info("接收{}发送的{}类型数据,数据签名：{}，时间戳：{}".format(address, data_type, signature, timestramp))

                elif data_type == "Heartbeat":
                    logger.info("接收{}发送的{}类型数据,数据签名：{}，时间戳：{}".format(address,data_type, signature,timestramp))

                else:
                    logger.info("接收{}发送的未知类型数据,数据签名：{}，时间戳：{}".format(address, data_type, signature, timestramp))

            except Exception as e:
                logger.error(e)
                pass

    def __heartbeat(self):
        while self.__running:
            for address in self.__remote_socket_list:
                if address:
                    self.send_msg_to("Heartbeat", "Heartbeat", address)
            time.sleep(5)

    def __pack_data(self,data, data_type="Data"):
        send_data_signature, send_time = self.__gen_data_signature(data)
        send_data = {"Type":data_type,"Data":data.decode("utf-8"), "Signature":send_data_signature,"Timestramp":send_time}
        return send_data

    def __unpack_data(self,data):
        recv_data = json.loads(data)
        return recv_data["Type"], recv_data["Data"], recv_data["Signature"], recv_data["Timestramp"]

    def __gen_data_signature(self, data):
        send_time = time.time()
        data_in_bytes = data + bytes("{}".format(send_time),'utf-8')
        hash_obj = md5()
        hash_obj.update(data_in_bytes)
        return hash_obj.hexdigest(), send_time


if __name__ == '__main__':
    rupd = RUDP()
    rupd.start()
    time.sleep(20)
    rupd.stop()
