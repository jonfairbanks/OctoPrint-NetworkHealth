# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import octoprint.plugin

class NetworkHealthPlugin(octoprint.plugin.StartupPlugin):
    def on_after_startup(self):
        self._logger.info("Beginning to monitor Network health...")


__plugin_name__ = "Network Health Monitor"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Monitors the health of the Network connection and restarts it if necessary"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = NetworkHealthPlugin()

def default_gateway():
    import socket, struct
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

def __init__():
    import os, time
    while True:
        def check_ping():
            hostname = default_gateway()
            response = os.system("ping -c 4 " + hostname)
            if response == 0:
                pingstatus = 0
            else:
                pingstatus = 1

            return pingstatus

        networkstatus = check_ping()

        if networkstatus == 1:
            self._logger.error("No Network Connection - Resetting Adapter(s)...")
            reset_wlan0 = 'ip link set wlan0 down; ip link set wlan0 up'
            reset_eth0  = 'ip link set eth0 down; ip link set eth0 up'
            os.system(reset_wlan0)
            os.system(reset_eth0)
            time.sleep(180)
            continue