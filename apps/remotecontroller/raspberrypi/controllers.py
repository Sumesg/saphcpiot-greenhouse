#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc


class ComponentController(object):
    """docstring for ComponentController"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, rpi_obj, logger):
        """Configure a new class

        @param rpi_obj: RPiObject subclass instance
        @param logger: ApplicationLogger instance
        """
        self.rpi_obj = rpi_obj
        self.logger = logger

    @property
    def rpi_obj(self):
        return self._rpi_obj

    @rpi_obj.setter
    def rpi_obj(self, value):
        self._rpi_obj = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    @classmethod
    @abc.abstractmethod
    def check(self, value):
        """Call abstract method

        Raises a NotImplementedError, because abstract methods can not be
        called.
        """
        raise NotImplementedError('Abstract method called')

    @classmethod
    @abc.abstractmethod
    def switch_off(self):
        raise NotImplementedError


class LampController(ComponentController):
    """LampController

    @param value: threshold value
    """
    def check(self, value):
        if value < 40:
            super().logger.info("Lamp Off")
            super().rpi_obj.lamp_off()
        else:
            super().logger.info("Lamp On")
            super().rpi_obj.lamp_on()

    def switch_state(self, op):
        if op == '1':
            super().logger.info("Lamp On")
            super().rpi_obj.lamp_on()
        else:
            super().logger.info("Lamp Off")
            super().rpi_obj.lamp_off()

    def switch_off(self):
        super().logger.info("switch off Lamp")
        super().rpi_obj.tearDownChannels()


class ServoController(ComponentController):
    """ServoController

    @param value: threshold value
    """
    def check(self, value):
        super().logger.info("Servo Motor Started")
        super().rpi_obj.start(value)

    def switch_off(self):
        super().logger.info("Servo Motor Stopped")
        super().rpi_obj.stop()


class RoofController(object):
    """docstring for RoofController"""
    def __init__(self, controller_obj):
        self.controller = controller_obj

    def open(self, value):
        self.controller.logger.info("Opening the roof...")
        self.controller.check(value)
        self.controller.logger.info("Roof opened!")

    def close(self):
        self.controller.logger.info("Closing the roof...")
        self.controller.switch_off()
        self.controller.logger.info("Roof closed!")
