"""Main runner"""
import logging
import os
import sys

from typing import List

import mcdata_to_json.configuration as Config
from mcdata_to_json.player import playerdata
from mcdata_to_json import LOGGER_NAME

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
_LOGGER = logging.getLogger(name=LOGGER_NAME)

Config.validatePaths()

UUIDS: List[str] = []
if (Config.PLAYERDATA_DIR not in Config.NONEXISTENT_FILES):
    UUIDS = list(map(lambda fn: fn.replace('.dat', ''),
                     os.listdir(Config.PLAYERDATA_DIR)))

_LOGGER.info("Found {} players".format(len(UUIDS)))
for uuid in UUIDS:
    playerdata.saveTempJSON(uuid)
