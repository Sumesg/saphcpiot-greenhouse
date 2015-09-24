#!/bin/bash

sudoProgID="sudo ./remote_app.py"
pythonProgID="python3 ./remote_app.py"
cleanup_folder="/home/pi/code/remotecontroller/"
cleanup="sudo ./cleanup_remotecontroller.py"

sudoPid=$(eval ps ax|grep "$sudoProgID"|grep -iv "grep"| awk '{print $1}')
echo "IoT Greenhouse Remote Controller sudo script pid = $sudoPid"

progPid=$(eval ps ax|grep "$pythonProgID"|grep -iv "grep"| awk '{print $1}')
echo "IoT Greenhouse Remote Controller main script pid = $progPid"

sudo kill -9 "$sudoPid"
if [ $? -eq 0 ]; then
    echo "Process $sudoPid was killed"
fi
sudo kill -9 "$progPid"
if [ $? -eq 0 ]; then
    echo "Process $progPid was killed"
fi
cd "$cleanup_folder"
$($cleanup)
if [ $? -eq 0 ]; then
    echo "GPIO pins cleaned"
fi

if [ -f /tmp/start_remotecontroller.log ]; then
  rm /tmp/start_remotecontroller.log
fi
if [ -f /tmp/stop_remotecontroller.log ]; then
  rm /tmp/stop_remotecontroller.log
fi
