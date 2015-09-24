#!/bin/bash

sudoProgID="sudo ./greenhous.py"
pythonProgID="python3 ./greenhouse.py"
cleanup_folder="/home/pi/code/greengarden/"
cleanup="sudo ./cleanup_greenhouse.py"

sudoPid=$(eval ps ax|grep "$sudoProgID"|grep -iv "grep"| awk '{print $1}')
echo "IoT Greenhouse sudo script pid = $sudoPid"

progPid=$(eval ps ax|grep "$pythonProgID"|grep -iv "grep"| awk '{print $1}')
echo "IoT Greenhouse main script pid = $progPid"

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

if [ -f /tmp/start_greenhouse.log ]; then
  rm /tmp/start_greenhouse.log
fi
if [ -f /tmp/stop_greenhouse.log ]; then
  rm /tmp/stop_greenhouse.log
fi
