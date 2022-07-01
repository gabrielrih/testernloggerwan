# testerNloggerWAN
It tests the WAN connection and it logs the status on every change.
The test connection works sending a ping packet to Google DNS server and if it fails try to send a second ping packet to the CloudFlare DNS Server.

## How to install it
Here we have a example of how to install it in a Linux machine. Just pay attention to install the latest version.

``cd /tmp``

``wget https://github.com/gabrielrih/testerNloggerWAN/archive/refs/tags/1.1.0.tar.gz``

``tar -xf 1.1.0.tar.gz``

``cd testerNlogger-1.1.0``

``sudo chmod 744 install.sh``

``sudo ./install.sh``

## Configuring the yml file (CallMeBot)
This repo use a Python library each sends free WhatsApp message.
To this works correctly you must edit the configuration file in /etc/.
The yml file looks like this:

```yml
- phone: +555598741585
  apikey: 152879
```

## How to check the log file?
``
tail -f /var/log/testernlogger/changeHistory.log
``


## Why using ping?
The idea was to use a simple and relyable mechanism to test the WAN connection. The use of a IP address in the ping command was to avoid to the scrip consider the WAN down when, for example, you have a DNS problem. As well, the ping packet is small so if your WAN connection is slow, the script continue considering the connection as up.

## What this repo doesn't do?
It doesn't identify when your connection is slow.
