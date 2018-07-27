#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os

def read_file(filename):
    file_info = open(os.path.join(os.getcwd(), "config", filename))
    infos = []
    for line_info in file_info:
        items = line_info.strip().split(",")
        if len(items) > 0:
            list_info = [i.decode("utf8") for i in items[1:]]
            infos.append((items[0].decode("utf8"), list_info))
    return infos


LOG_FORMAT = "%(asctime)s|%(filename)s|%(lineno)s|%(levelname)s| %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

log_info = read_file("log_info.txt")

logging.basicConfig(filename=log_info[1][1][0], level=eval("logging.%s" % log_info[0][1][0]), format=LOG_FORMAT, datefmt=DATE_FORMAT)

INFO = logging.info
WARN = logging.warning
ERROR = logging.error
DEBUG = logging.debug