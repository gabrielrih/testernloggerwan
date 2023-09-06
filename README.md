# testernlogger
It tests the WAN connection and logs the status on every change.
The connection process works building a socket to Google DNS server and if fails the WAN connection is considered as down.

## Contents
- [Installation and usage](#installation-and-usage)
    - [How to install it](#how-to-install-it)
    - [How to check the log file](#how-to-check-the-log-file)
    - [How to change some configuration](#how-to-change-some-configuration)
    - [Receiving notification by WhatsAPP](#receiving-notification-by-whatsapp)
- [Development](#development)
    - [Using Docker](#using-docker)
    - [Running in your machine](#runnnig-in-your-machine)

## Installation and usage
### How to install it
Here we have a example of how to install it in a Linux machine. Just pay attention to install the latest version.

```sh
cd /tmp
wget https://github.com/gabrielrih/testerNloggerWAN/archive/refs/tags/X.X.X.tar.gz
tar -xf X.X.X.tar.gz
cd testerNloggerWAN-X.X.X
sudo chmod 744 install.sh
sudo ./install.sh
```

When the installation finished you'll have a Linux service running and monitoring your WAN connection.

```sh
sudo systemctl status testernlogger
```


### How to check the log file
```sh
tail -f /var/log/testerNlogger/testerNlogger.log
```

... or use the local configured on the instalation


### How to change some configuration
If you want to change some configuration, the default config file is "/etc/testerNlogger/config.ini" (you can change this folder in installation).

```sh
sudo vi /etc/testerNlogger/config.ini
```

After you change it, you must restart the service

```sh
sudo systemctl restart testernlogger
sudo systemctl status testernlogger
```


### Receiving notification by WhatsAPP
In the config file you have a group called "NOTIFICATION". In this group you can configure you phone number to receive notifications in WhatsApp everytime the WAN connection turns UP.

Is important to comment that you must authorize the CallMeBot to send messages to your phone number. To do this you must follow this [link](https://www.callmebot.com/blog/free-api-whatsapp-messages/).


```yaml
[NOTIFICATION]
ENABLE_NOTIFICATION = True
ENABLE_FAKE_MODE = False
PHONE_NUMBER = +555599887766
API_KEY = 123456
```

## Development
### Using Docker

Before you run it, we must create a custom config.ini file for testing:
```sh
cp config/config-example.ini config/config.ini
```

Then, you can create a container to run the script:

```sh
docker compose up --build -d
```

The compose will create and run a container and sync the logs from _/var/log/testerNlogger/_ to _./log/_

If you want to connect to the container you can run:

```sh
docker exec -it testernlogger /bin/bash
```

### Running in your machine

Before you run it, we must create a custom config.ini file for testing:
```sh
cp config/config-example.ini config/config.ini
```

If you want to run in your machine you must install the depedencies and then run the script:

```sh
pip install -r requirements/commons.txt
python testerNlogger.py --config config/config.ini
```

You also can enable the debug mode:

```sh
python testerNlogger.py --config config/config.ini --debug
```
