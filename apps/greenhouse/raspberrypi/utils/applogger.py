#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import logging.handlers


class ApplicationLogger(object):
    @staticmethod
    def init_logger(log_file):
        try:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            # create a file handler
            handler = logging.handlers.TimedRotatingFileHandler(log_file, when="midnight", backupCount=5)
            handler.setLevel(logging.INFO)
            # create a logging format
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            # add the handlers to the logger
            logger.addHandler(handler)
            return logger
        except KeyboardInterrupt:
            # handle Ctrl-C
            logging.warn("Cancelled by user")
        except Exception as ex:
            # handle unexpected script errors
            logging.exception("Unhandled error\n{}".format(ex))
            raise
        finally:
            # perform an orderly shutdown by flushing and closing all handlers;
            # called at application exit and no further use of the logging
            # system should be made after this call.
            logging.shutdown()


# Make a class we can use to capture stdout and sterr in the log
class StdOutErrLogger(object):
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level

    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())
