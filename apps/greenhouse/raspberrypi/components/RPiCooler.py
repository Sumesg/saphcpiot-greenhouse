#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .RPiObject import RPiObject


class RPiCooler(RPiObject):
    """docstring for RPiCooler"""
    def __init__(self, init_pin):
        RPiObject.__init__()
        self.init_cooler_pin = init_pin
        super(RPiCooler, self).setup(self.init_cooler_pin)

    def cooler_on(self):
        self._cooler_on()

    def cooler_off(self):
        self._cooler_off()

    def _cooler_on(self):
        super(RPiCooler, self).output_on(self.init_cooler_pin)

    def _cooler_off(self):
        super(RPiCooler, self).output_off(self.init_cooler_pin)
