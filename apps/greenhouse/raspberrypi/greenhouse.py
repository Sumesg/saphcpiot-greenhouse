#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import argparse
import configs  # all configuration settings come from configs.py
from utils.applogger import ApplicationLogger, StdOutErrLogger
from application import Application


def get_app_arguments():
    # Configure the arguments to execute the script
    parser = argparse.ArgumentParser(description="IoT Garden Main Script")
    parser.add_argument("-d", "--demo", help="Sleep time for demo mode")
    parser.add_argument("-p", "--proxies", help="SAP Proxies", action="append")
    return parser.parse_args()


def main(app_arguments, config_file, logger_obj):
    app = Application(app_arguments, config_file, logger_obj)
    app.run()


if __name__ == "__main__":
    # Script Arguments\
    args = get_app_arguments()
    # Logger instance
    logger = ApplicationLogger.init_logger(configs.log_file_path)
    # Replace stdout with logging to file at INFO level
    sys.stdout = StdOutErrLogger(logger, logging.INFO)
    # Replace stderr with logging to file at ERROR level
    sys.stderr = StdOutErrLogger(logger, logging.ERROR)
    # Execute the application
    main(args, configs, logger)
