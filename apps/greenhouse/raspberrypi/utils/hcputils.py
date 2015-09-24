#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests


class HCPUtils:

    def __init__(self, iotmms, device_id, device_token, message_type_id, logger):
        self.iotmms = iotmms
        self.device_id = device_id
        self.device_token = device_token
        self.message_type_id = message_type_id
        self.logger = logger

    def publishSensorValues(self, temp, hum):
        self.logger.info("Sending data to HCP...")
        return self._saveSensorValues(temp, hum)

    def _saveSensorValues(self, temp, hum):
        r = requests.post(self._buildURL(),
                          headers=self._buildHeaders(),
                          data=self._buildPayload(temp, hum))
        if r.status_code != 200:
            self.logger.exception("Problem occurs sending data to HCP %s" % r.status_code)
            self.logger.exception("Error: %s" % r.json())
            sys.exit(1)
        else:
            self.logger.info("Saved! %s" % r.json())

    def _buildHeaders(self):
        return {'Authorization': 'Bearer ' + self.device_token,
                'Content-Type': 'application/json;charset=utf-8'}

    # Return a dict ready to be used as query params
    def _buildPayload(self, temp, hum):
        return '{"mode":"sync", "messageType":%s, "messages":[{"temperature": %s, "humidity": %s}]}' % (self.message_type_id, temp, hum)

    # Load the properties file and return a valid HCP url
    def _buildURL(self):
        return self.iotmms + self.device_id
