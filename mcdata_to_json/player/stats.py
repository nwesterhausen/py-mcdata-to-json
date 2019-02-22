"""Code to parse stats.json files"""
"""Code to parse player advancements"""

import os
import re
import json
import logging
from typing import Dict

import mcdata_to_json.configuration as Config
from mcdata_to_json import LOGGER_NAME

_LOGGER = logging.getLogger(name=LOGGER_NAME)


def save_temp_stats_json(uuid: str) -> Dict:
    filepath = os.path.join(Config.ADVANCEMENTS_DIR, "{}.json".format(uuid))
    _LOGGER.debug("Trying to open {}".format(filepath))
    with open(filepath, 'r') as sf:
        parsedJson = json.load(sf)
        parsedJson.pop('DataVersion', '')
        jsadv = json.dumps(parsedJson)
        with open(
                os.path.join(Config.TEMP_STATS_JSON_DIR,
                             "{}.json".format(uuid)), 'w') as ad:
            ad.write(jsadv)
            _LOGGER.debug("Saved parsed Stats for {}".format(uuid))