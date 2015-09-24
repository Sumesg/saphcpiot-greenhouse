#!/bin/bash

path="/home/pi/code/remotecontroller/"
sudoProgID="sudo ./remote_app.py"

cd "$path"
echo "Starting IoT Greenhouse Remote Controller..."
$($sudoProgID)
