#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

LOG_FORMAT = "%(asctime)s|%(levelname)s| %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

logging.basicConfig(filename='run.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

INFO = logging.info
WARN = logging.warning
ERROR = logging.error