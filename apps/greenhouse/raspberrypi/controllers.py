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


class LedStripController(ComponentController):
    """docstring for LedStripController"""

    """ Check

    @param value: threshold value
    """
    def check(self, value):
        if value < 18:
            super().logger.info("Leds all On")
            super().rpi_obj.allOn()
        elif (value >= 18) and (value < 20):
            super().logger.info("Yellow")
            super().rpi_obj.yellow()
        elif (value >= 20) and (value < 25):
            super().logger.info("Green")
            super().rpi_obj.green()
        elif value >= 25:
            super().logger.info("Red")
            super().rpi_obj.red()
        else:
            super().logger.info("Leds all Off")
            super().rpi_obj.allOff()

    def switch_off(self):
        super().logger.info("switch off Leds")
        super().rpi_obj.tearDownChannels()
