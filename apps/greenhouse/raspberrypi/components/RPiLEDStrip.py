#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .RPiObject import RPiObject


class RPiLEDStrip(RPiObject):
    """docstring for RPiLED"""
    def __init__(self, green_pin, yellow_pin, red_pin):
        self.green_led_pin = green_pin
        self.yellow_led_pin = yellow_pin
        self.red_led_pin = red_pin
        super().__init__()

        super().setup(self.green_led_pin)
        super().setup(self.yellow_led_pin)
        super().setup(self.red_led_pin)

    def yellow(self):
        self._green_off()
        self._yellow_on()
        self._red_off()

    def green(self):
        self._green_on()
        self._yellow_off()
        self._red_off()

    def red(self):
        self._green_off()
        self._yellow_off()
        self._red_on()

    def allOff(self):
        self._green_off()
        self._yellow_off()
        self._red_off()

    def allOn(self):
        self._green_on()
        self._yellow_on()
        self._red_on()

    def _green_on(self):
        super().output_on(self.green_led_pin)

    def _green_off(self):
        super().output_off(self.green_led_pin)

    def _yellow_on(self):
        super().output_on(self.yellow_led_pin)

    def _yellow_off(self):
        super().output_off(self.yellow_led_pin)

    def _red_on(self):
        super().output_on(self.red_led_pin)

    def _red_off(self):
        super().output_off(self.red_led_pin)
