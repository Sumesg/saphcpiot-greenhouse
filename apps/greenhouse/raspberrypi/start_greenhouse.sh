#!/bin/bash

path="/home/pi/code/greengarden/"
sudoProgID="sudo ./greenhouse.py"

cd "$path"
echo "Starting IoT Greenhouse Demo..."
$($sudoProgID)
