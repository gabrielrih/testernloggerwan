#!/bin/bash
#
# Tester N Logger
# It test and log the wan connection status.
# By gabrielrih <gabrielrih@gmail.com>
#

INTERVAL_TO_TEST_CONNECTION_IN_SECONDS=10
LOG_FOLDER="/var/log/testerNlogger"
LOG_FILENAME="connection.log"
LOG_WHEN_CHANGE_FILENAME="changeHistory.log"
LOG_FULL_PATH=$LOG_FOLDER/$LOG_FILENAME
LOG_ON_CHANGE_FULL_PATH=$LOG_FOLDER/$LOG_WHEN_CHANGE_FILENAME
CLEAR_LOG_FILES_EVERY_START=false # for testing usage

# RUN AS ADMIN

testConnection() {
    ping 8.8.8.8 -c 1 > .result.tmp
    isDown=$(cat .result.tmp | grep "100% packet loss" | wc -l)
    return $isDown
}

createLogContent() {
    if [ $isDown -eq 1 ]; then status='down'; else status='up'; fi
    logContent="$(date +%Y-%m-%d)|$(date +%H:%M:%S)|$status|"
}

logWhenStatusChanged() {
    if [ ! $isDownLast ]; then isDownLast=2; fi # first execution. Force value two to print changed log
    # log file. Format: date|time|status|
    if [ ! -f $LOG_ON_CHANGE_FULL_PATH ]; then echo "date|time|status|" >> $LOG_ON_CHANGE_FULL_PATH; fi # print header if log file doesn't exists
    createLogContent
    if [ $isDown -ne $isDownLast ]; then echo $logContent >> $LOG_ON_CHANGE_FULL_PATH; fi
    # set current as last
    isDownLast=$isDown
}

logEverything() {
    # standard stdout
    if [ $isDown -eq 1 ]; then echo "[-] Connection is DOWN! ($currentDatetime)"; else echo "[+] Connection is UP! ($currentDatetime)"; fi
    # log file. Format: date|time|status|
    if [ ! -f $LOG_FULL_PATH ]; then echo "date|time|status|" >> $LOG_FULL_PATH; fi # print header if log file doesn't exists
    createLogContent
    echo $logContent >> $LOG_FULL_PATH
}

cleaningLogFiles() {
    echo "[!] Cleaning old log files!"
    rm $LOG_FULL_PATH
    rm $LOG_ON_CHANGE_FULL_PATH
}

echo "Testing WAN connection every $INTERVAL_TO_TEST_CONNECTION_IN_SECONDS seconds..."
if [ $CLEAR_LOG_FILES_EVERY_START == true ]; then cleaningLogFiles; fi
while true
do
    currentDatetime=$(date +%Y-%m-%dT%H:%M:%S)
    testConnection
    if [ ! -d $LOG_FOLDER ]; then mkdir $LOG_FOLDER; fi
    logWhenStatusChanged
    logEverything
    sleep $INTERVAL_TO_TEST_CONNECTION_IN_SECONDS
done

exit 0