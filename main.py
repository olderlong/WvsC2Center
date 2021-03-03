#! /usr/bin/env python
# _*_coding:utf-8 -*_

import os
import click

from app import create_app
from app.scan_session import GlobalVar

app = create_app(os.getenv('FLASK_CONFIG') or 'production')


@click.command()
@click.option('--host', default=app.config["HOST"], help="Web服务器IP地址")
@click.option('--port', default=app.config["PORT"], help="Web服务器端口")
def main(host, port):
    """启动主函数

    Args:
        host (str): 命令行参数，为Web服务器主机ip地址
        port (int): 命令行参数，为Web服务器主机端口
    """
    GlobalVar.SocketIO.run(app=app, host=host, port=port, use_reloader=False)


if __name__ == '__main__':
    main()
