#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .RPiObject import RPiObject


class RPiLamp(RPiObject):
    """docstring for RPiLAMP"""
    def __init__(self, init_pin):
        self.init_lamp_pin = init_pin
        super().__init__()
        super().setup(self.init_lamp_pin)

    def lamp_on(self):
        self._lamp_on()

    def lamp_off(self):
        self._lamp_off()

    def _lamp_on(self):
        super().output_off(self.init_lamp_pin)

    def _lamp_off(self):
        super().output_on(self.init_lamp_pin)
