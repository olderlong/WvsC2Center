#! /usr/bin/env python
# _*_coding:utf-8 -*_
import os
import logging
import time
import sys

basedir = os.path.abspath(os.path.dirname(__file__))


def singleton(cls):
    """单例模式修饰器

    Returns:
        object : 单例对象
    """
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


def init_logger(name):
    """初始化日志记录器

    Args:
        name (str): 日志记录器名称
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(pathname)s [line:%(lineno)d] %(levelname)s >>> %(message)s'
    )
    # 文件日志
    file_handler = logging.FileHandler(
        os.path.join(
            basedir, "log/{}.log".format(
                time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime(time.time())))))
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


class BaseConfig(object):
    """Web服务器基本配置类

    Args:
        object (object): 基类
    """
    # 密钥，用于防止跨站脚本攻击
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or "pBw%E7feV!!tJZuP3f&QPz2%ola*2IyE"
    # 扫描任务目录
    SCAN_TASK_PATH = os.path.join(basedir, "scan_task")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    """开发配置类

    Args:
        BaseConfig (BaseConfig): Web服务器配置基类
    """
    DEBUG = True
    PORT = 5000
    HOST = "127.0.0.1"

    @staticmethod
    def init_app(app):
        # app.debug = DevelopmentConfig.DEBUG
        # app.port = DevelopmentConfig.PORT
        # app.host = DevelopmentConfig.HOST
        init_logger("Server")


class TestingConfig(BaseConfig):
    """测试配置类

    Args:
        BaseConfig (BaseConfig): Web服务器配置基类
    """
    TEST = True
    PORT = 5000
    HOST = "127.0.0.1"


class ProductionConfig(BaseConfig):
    """产品配置类，为最终部署时配置类

    Args:
        BaseConfig (BaseConfig): Web服务器配置基类
    """
    # 关闭调试模式
    DEBUG = False
    # Web服务端口
    PORT = 80
    # Web服务器IP，更换服务器时需要修改该IP
    HOST = "192.168.43.137"

    @staticmethod
    def init_app(app):
        """初始化Web应用

        Args:
            app (app): Flask app
        """
        app.debug = ProductionConfig.DEBUG
        app.port = ProductionConfig.PORT
        app.host = ProductionConfig.HOST

        # 初始化日志记录器
        init_logger("Server")
        logger = logging.getLogger("Server")
        logger.info("Web Server is running <{}:{}>...".format(
            ProductionConfig.HOST, ProductionConfig.PORT))


web_server_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
