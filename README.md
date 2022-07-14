# testerNloggerWAN
It tests the WAN connection and logs the status on every change.
The connection process works building a socket to Google DNS server and if fails the WAN connection is considered as down.

## How to install it
Here we have a example of how to install it in a Linux machine. Just pay attention to install the latest version.

``cd /tmp``

``wget https://github.com/gabrielrih/testerNloggerWAN/archive/refs/tags/X.X.X.tar.gz``

``tar -xf X.X.X.tar.gz``

``cd testerNloggerWAN-X.X.X``

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


# For dev environment

You can manually start the script running this command:

``
python3 testerNlogger.py --config config/config.ini
``

Remember to point the --config argument to your config file.

You also can enable the debug mode:

``
python3 testerNlogger.py --config config/config.ini --debug
``