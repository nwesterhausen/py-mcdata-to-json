"""Code to grab player profile information from Mojang"""

import os
import re
import json
import logging
from typing import Dict, List

import mcdata_to_json.configuration as Config
from mcdata_to_json import LOGGER_NAME

_LOGGER = logging.getLogger(name=LOGGER_NAME)
