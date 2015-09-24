#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
import configs  # all configuration settings come from configs.py
import requests
import time
import subprocess
from components.RPiLamp import RPiLamp
from utils.applogger import ApplicationLogger, StdOutErrLogger
from controllers import LampController


class RemoteControllerApp(object):
    def __init__(self, configs, logger):
        self.configs = configs
        self.logger = logger

    def run(self):
        lamp_controller = None
        try:
            lamp = self._create_objects()
            lamp_controller = LampController(lamp, self.logger)
            # MAIN LOOP
            while True:
                self._commands_controller(lamp_controller)
                time.sleep(3)  # every 3 seconds
        except Exception:
            self.logger.exception("Exception: %s", sys.exc_info()[1])
        except KeyboardInterrupt:
            self.logger.warn("Cancelled by user: %s", sys.exc_info()[1])
        finally:
            lamp_controller.switch_off()

    def _commands_controller(self, oController):
        r = requests.get(self._buildURL(), headers=self._buildHeaders())
        response = r.json()
        if response:  # if IoT Service response is not an empty array
            self._retrieve_messages(response, oController)

    def _buildURL(self):
        return self.configs.iot_url + self.configs.device_id

    def _buildHeaders(self):
        return {
            'Authorization': 'Bearer ' + self.configs.device_token,
            'Content-Type': 'application/json;charset=utf-8'
        }

    def _create_objects(self):
        _lamp = RPiLamp(self.configs.lamp_pin)
        return _lamp

    def _retrieve_messages(self, response, oController):
        oController.switch_state('0')  # switch off at starts
        messages = response[0]['messages']
        for m in messages:
            self._acts(m, oController)

    def _acts(self, m, controller):
        if m['opcode'] == 'lamp':
            controller.switch_state(m['operand'])
        elif m['opcode'] == 'roof':
            print('roof...')
