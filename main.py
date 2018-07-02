#! /usr/bin/env python
# _*_coding:utf-8 -*_

import os

from app import create_app

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app(os.getenv('FLASK_CONFIG') or 'production')

if __name__ == '__main__':
    # manager.run()
    app.run(host="0.0.0.0", port=80)

