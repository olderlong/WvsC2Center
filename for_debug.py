import time

from app.ccserver import CCServerConfig
from app.ccserver import CliApp

if __name__ == '__main__':
    CCServerConfig.load_config()
    print(CCServerConfig.Address)
    CliApp().run()
    time.sleep(20)