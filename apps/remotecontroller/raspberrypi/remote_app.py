#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# all configuration settings come from configs.py
import sys
import logging
import configs
from utils.applogger import ApplicationLogger, StdOutErrLogger
from remotecontroller import RemoteControllerApp


def main(config_file, logger_obj):
    app = RemoteControllerApp(config_file, logger_obj)
    app.run()


# Logger instance
logger = ApplicationLogger.init_logger(configs.remote_controller_file_path)
# Replace stdout with logging to file at INFO level
sys.stdout = StdOutErrLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = StdOutErrLogger(logger, logging.ERROR)
# Execute the application
main(configs, logger)
