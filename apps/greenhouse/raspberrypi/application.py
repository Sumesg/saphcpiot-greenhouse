#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

from utils.dhtutils import DHTUtils
from utils.hcputils import HCPUtils
from components.RPiLEDStrip import RPiLEDStrip
from components.RPiLamp import RPiLamp
from components.RPiServo import RPiServo
from controllers import LedStripController, LampController


class Application(object):
    def __init__(self, args, configs, logger):
        self.args = args
        self.configs = configs
        self.logger = logger

    def run(self):
        try:
            # Instantiate objects
            dht, leds, hcp = self._create_objects()
            # Instantiate Controllers
            leds_controller = LedStripController(leds, self.logger)

            # MAIN LOOP
            while True:
                dht.read_sensor()
                temperature, humidity = dht.retrieve_values()
                # using controllers
                leds_controller.check(temperature)
                hcp.publishSensorValues(temperature, humidity)
                # Wait
                self._set_sleep_time(self.args.demo)
        except Exception:
            self.logger.exception("Exception: %s", sys.exc_info()[1])
        except KeyboardInterrupt:
            self.logger.warn("Cancelled by user: %s", sys.exc_info()[1])
        finally:
            leds_controller.switch_off()

    def _create_objects(self):
        _dht = DHTUtils(self.configs.sensor_type,
                        self.configs.sensor_data_pin,
                        self.logger)
        _leds = RPiLEDStrip(self.configs.green_led_pin,
                            self.configs.yellow_led_pin,
                            self.configs.red_led_pin)
        _hcp = HCPUtils(self.configs.iot_url, self.configs.device_id,
                        self.configs.device_token, self.logger)
        return _dht, _leds, _hcp

    def _set_sleep_time(self, param):
        if(param):
            time.sleep(self.configs.demotime)  # Wait 30 seconds
        else:
            time.sleep(self.configs.standardtime)  # Wait 30 minutes
