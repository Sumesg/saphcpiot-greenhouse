#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .RPiObject import RPiObject


class RPiServo(RPiObject):
    """RPiServo

    @param pin: gpio pin
    @param frequency:
    """
    def __init__(self, pin, frequency):
        self.data_pin = pin
        self.frequency = frequency
        super().__init__()
        super().setup(self.data_pin)
        self.pwm = super().GPIO.PWM(self.data_pin, self.frequency)

    """
    @param value: the duty cycle (0.0 <= dc <= 100.0)
    """
    def start(self, value):
        self.pwm.start(value)

    def stop(self):
        super().tearDownChannels()
