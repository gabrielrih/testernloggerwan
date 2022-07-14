# testerNloggerWAN
It tests the WAN connection and it logs the status on every change.
The test connection works building a socker to Google DNS server and if it fails consider the WAN connection as down.

## How to install it
Here we have a example of how to install it in a Linux machine. Just pay attention to install the latest version.

``cd /tmp``

``wget https://github.com/gabrielrih/testerNloggerWAN/archive/refs/tags/2.0.0.tar.gz``

``tar -xf 2.0.0.tar.gz``

``cd testerNloggerWAN-2.0.0``

``sudo chmod 744 install.sh``

``sudo ./install.sh``

When the installation finished you'll have a Linux service running and monitoring your WAN connection.

``
sudo systemctl status testernlogger
``


## How to check the log file?
``
tail -f /var/log/testerNlogger/testerNlogger.log
``


## How to change some configuration
If you want to change some configuration, the default config file is "/etc/testerNlogger/config.ini" (you can change this folder in installation).

``
sudo vi /etc/testerNlogger/config.ini
``

After you change it, you must restart the service

``
sudo systemctl restart testernlogger
sudo systemctl status testernlogger
``


## Receiving notification by WhatsAPP
In the config file you have a group called "NOTIFICATION". In this group you can configure you phone number to receive notifications in WhatsApp everytime the WAN connection turns UP.

Is important to comment that you must authorize the CallMeBot to send messages to your phone number. To do this you must follow this [link](https://www.callmebot.com/blog/free-api-whatsapp-messages/).


```
[NOTIFICATION]
ENABLE_NOTIFICATION = True
ENABLE_FAKE_MODE = False
PHONE_NUMBER = +555599887766
API_KEY = 123456
```