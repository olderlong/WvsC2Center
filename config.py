#! /usr/bin/env python
# _*_coding:utf-8 -*_
import os
import logging
import time
import sys

basedir = os.path.abspath(os.path.dirname(__file__))


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


def init_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(pathname)s [line:%(lineno)d] %(levelname)s >>> %(message)s')
    # 文件日志
    file_handler = logging.FileHandler(
        os.path.join(
            basedir,
            "log/{}.log".format(
                time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime(time.time())))))
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "pBw%E7feV!!tJZuP3f&QPz2%ola*2IyE"
    SCAN_TASK_PATH = os.path.join(basedir, "scan_task")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    PORT = 5000
    HOST = "127.0.0.1"
    # SERVER_NAME = "{}:{}".format(HOST, PORT)


    @staticmethod
    def init_app(app):
        # app.debug = DevelopmentConfig.DEBUG
        # app.port = DevelopmentConfig.PORT
        # app.host = DevelopmentConfig.HOST

        init_logger("Server")


class TestingConfig(BaseConfig):
    TEST = True
    PORT = 5000
    HOST = "127.0.0.1"
    # SERVER_NAME = "{}:{}".format(HOST, PORT)


class ProductionConfig(BaseConfig):
    DEBUG = False
    PORT = 80
    HOST = "192.168.3.2"
    HOST = "192.168.1.31"
    # SERVER_NAME = "{}:{}".format(HOST, PORT)

    @staticmethod
    def init_app(app):
        # app.debug = DevelopmentConfig.DEBUG
        # app.port = DevelopmentConfig.PORT
        # app.host = DevelopmentConfig.HOST

        init_logger("Server")


web_server_config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }