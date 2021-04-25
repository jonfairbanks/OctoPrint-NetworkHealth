# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin

class WifiHealthPlugin(octoprint.plugin.StartupPlugin):
    def on_after_startup(self):
        self._logger.info("Beginning to monitor Wifi health...")


__plugin_name__ = "Wifi Health Monitor"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Monitors the health of the Wifi connection and restarts it if necessary"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = WifiHealthPlugin()

def __init__():
    import os
    import time

    while True:
        def check_ping():
            hostname = "192.168.1.1"
            response = os.system("ping -c 4 " + hostname)
            if response == 0:
                pingstatus = 0
            else:
                pingstatus = 1

            return pingstatus

        networkstatus = check_ping()

        if networkstatus == 1:
            self._logger.error("No Wireless Connection - Resetting Adapter(s)...")
            wlan_down = 'ip link set wlan0 down'
            wlan_up  = 'ip link set wlan0 up'
            os.system(wlan_down)
            os.system(wlan_up)
            time.sleep(180)
            continue