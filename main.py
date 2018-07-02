#! /usr/bin/env python
# _*_coding:utf-8 -*_

import os
import click

from app import create_app

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app(os.getenv('FLASK_CONFIG') or 'production')


@click.command()
@click.option('--host', default="127.0.0.1", help="Web服务器IP地址")
@click.option('--port', default=5000, help="Web服务器端口")
def main(host, port):
    app.run(host=host, port=port, use_reloader=False)


if __name__ == '__main__':
    main()

