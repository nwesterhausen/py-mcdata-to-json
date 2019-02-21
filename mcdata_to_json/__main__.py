"""Main runner"""
import logging
import sys

import mcdata_to_json.configuration as Config
from mcdata_to_json import LOGGER_NAME

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
_LOGGER = logging.getLogger(name=LOGGER_NAME)

Config.validatePaths()
