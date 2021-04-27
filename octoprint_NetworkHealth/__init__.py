import os
import time
import octoprint

from octoprint.util import RepeatedTimer

class NetworkHealthPlugin(octoprint.plugin.StartupPlugin, octoprint.plugin.RestartNeedingPlugin):
    def __init__(self):
        self._timer = None

    def on_after_startup(self):
        self._logger.info("Beginning to monitor Network health...")
        self._timer = RepeatedTimer(180, self._check_network)
        self._timer.start()

    def _check_network(self):
        try:
              if not self.check_ping():
                  self._logger.error("No Network Connection - Resetting Adapter(s)...")
                  reset_wlan0 = 'sudo ip link set wlan0 down; sudo ip link set wlan0 up'
                  reset_eth0  = 'sudo ip link set eth0 down; sudo ip link set eth0 up'
                  os.system(reset_wlan0)
                  os.system(reset_eth0)
        except Exception:
            self._logger.exception("Could not run network health check")

    def get_update_information(self):
        return dict(
            networkhealth=dict(
                displayName=self._plugin_name,
                displayVersion=self._plugin_version,

                type="github_release",
                current=self._plugin_version,
                user="jonfairbanks",
                repo="OctoPrint-NetworkHealth",

                pip="https://github.com/jonfairbanks/OctoPrint-NetworkHealth/archive/{target}.zip"
            )
        )

    def default_gateway(self):
        import socket
        import struct
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    continue
                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

    def check_ping(self):
        hostname = self.default_gateway()
        response = os.system("ping -c 4 " + hostname)
        if response == 0:
            return True
        else:
            return False


__plugin_name__ = "Network Health Monitor"
__plugin_version__ = "1.0.1"
__plugin_description__ = "Monitors the health of the Network connection and restarts it if necessary"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_check__():
    import sys

    if not sys.platform.startswith("linux"):
        import logging
        logging.getLogger("octoprint.plugins.networkhealth").error("Cannot run this plugin under anything but Linux")
        return False

    return True

def __plugin_load__():
    global __plugin_implementation__
    global __plugin_hooks__

    __plugin_implementation__ = NetworkHealthPlugin()
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
