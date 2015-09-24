#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess


class DHTUtils:
    """
     Read sensor data using the Adafruit utility
     Output example: Temp=20.0*C  Humidity=56.9%

     Parameters:
        type - sensor type -> 11 = DHT11; 22 = DHT22
        pin_number - GPIO pin number for data

     Returns:
        float - temperature
        float - humidity
    """

    ADAFRUIT = "/home/pi/Adafruit/Adafruit_Python_DHT/examples/AdafruitDHT.py"

    def __init__(self, sensor_type, pin_number, logger):
        self.sensor_type = sensor_type
        self.pin_number = pin_number
        self.logger = logger
        self.result = ""

    def _strip_output(self, output):
        self.logger.info(output)
        # Temperature
        index = output.find("Temp=")
        index_2 = output.find("*C")
        if index == -1 or index_2 == -1:
            return False, 0.0, 0.0
        temperature = float(output[index + 5: index_2])

        # Humidity
        index = output.find("Humidity=")
        if index == -1:
            return False, 0.0, 0.0
        humidity = float(output[index + 9:-2])

        return True, temperature, humidity

    def read_sensor(self):
        # execute the Adafruit utility
        outputbytes = subprocess.check_output(["sudo", self.ADAFRUIT,
                                               str(self.sensor_type),
                                               str(self.pin_number)])

        # Use the decode function to convert a byte sequence into string
        output = outputbytes.decode("utf-8")

        self.result = self._strip_output(output)

    def retrieve_values(self):
        return self.result[1], self.result[2]
