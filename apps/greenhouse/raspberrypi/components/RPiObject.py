#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO


class RPiObject(object):
    """docstring for RPiObject"""
    def __init__(self):
        self.GPIO = GPIO
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)

    @property
    def GPIO(self):
        return self._gpio

    @GPIO.setter
    def GPIO(self, value):
        self._gpio = value

    def tearDownChannels(self):
        self.GPIO.cleanup()

    def setup(self, pin_number):
        self.GPIO.setup(pin_number, self.GPIO.OUT)

    def output_on(self, pin_number):
        self.GPIO.output(pin_number, self.GPIO.HIGH)

    def output_off(self, pin_number):
        self.GPIO.output(pin_number, self.GPIO.LOW)
