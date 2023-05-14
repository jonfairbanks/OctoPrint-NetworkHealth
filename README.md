# OctoPrint-NetworkHealth

![GitHub top language](https://img.shields.io/github/languages/top/jonfairbanks/OctoPrint-NetworkHealth.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/jonfairbanks/OctoPrint-NetworkHealth.svg)
![License](https://img.shields.io/github/license/jonfairbanks/OctoPrint-NetworkHealth.svg?style=flat)

#### Monitors the health of the OctoPrint Network connection and restarts it if necessary

### Configuration

By default the `ip` command used to restart the network interfaces requires sudo permissions. 

To allow OctoPrint to manage this for us, we need to update sudoers using the below command:
```
echo 'pi ALL=NOPASSWD:/sbin/ip' | sudo tee /etc/sudoers.d/octoprint-ip
```

If your system does not have `ip` installed, you can install it via apt:
```
apt-get install iproute2
```

### Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/jonfairbanks/OctoPrint-NetworkHealth/archive/master.zip
