#! /usr/bin/env python
# _*_coding:utf-8 -*_

import os
import click

from app import create_app
from app.scan_session import GlobalVar


# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app(os.getenv('FLASK_CONFIG') or 'production')

# @click.option('--host', default="127.0.0.1", help="Web服务器IP地址")
# @click.option('--port', default=5000, help="Web服务器端口")
@click.command()
@click.option('--host', default=app.config["HOST"], help="Web服务器IP地址")
@click.option('--port', default=app.config["PORT"], help="Web服务器端口")
def main(host, port):
    # app.run(host=host, port=port, use_reloader=False)
    # app.config.update(HOST=host)
    # app.config.update(PORT=port)
    # app.run(host=app.config["HOST"], port=app.config["PORT"],use_reloader=False)
    GlobalVar.SocketIO.run(app=app, host=host, port=port, use_reloader=False)
    # GlobalVar.SocketIO.run(app=app, host=app.config["HOST"], port=app.config["PORT"], use_reloader=False)

if __name__ == '__main__':
    main()

