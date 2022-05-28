# -*- coding: utf-8 -*-

import os, logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

def create_log(name):
    logfmt = '%(asctime)s [%(levelname)s](%(module)s:%(lineno)d) %(message)s'
    logging.basicConfig(level=logging.INFO, format=logfmt)
    uvlogger = logging.getLogger(name)

    script_dir = Path( __file__ ).parent.absolute()    
    logfile = name + ".log"
    logpath = script_dir / logfile

    handler = RotatingFileHandler(logpath, maxBytes=1000000, backupCount=5)
    formatter = logging.Formatter(logfmt)
    handler.setFormatter(formatter)
    uvlogger.addHandler(handler)    
    return uvlogger
