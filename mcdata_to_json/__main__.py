"""Main runner"""
import logging
import os
import sys
import asyncio

from typing import List

import mcdata_to_json.configuration as Config
import mcdata_to_json.mojang_api as mojang_api
from mcdata_to_json.player import playerdata, advancements
from mcdata_to_json import LOGGER_NAME

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
_LOGGER = logging.getLogger(name=LOGGER_NAME)

Config.validatePaths()

UUIDS: List[str] = []
if (Config.PLAYERDATA_DIR not in Config.NONEXISTENT_FILES):
    UUIDS = list(
        map(lambda fn: fn.replace('.dat', ''),
            os.listdir(Config.PLAYERDATA_DIR)))

_LOGGER.info("Found {} players".format(len(UUIDS)))
for uuid in UUIDS:
    playerdata.save_temp_playerdata_json(uuid)
    advancements.save_temp_advancement_json(uuid)

loop = asyncio.get_event_loop()
loop.run_until_complete(mojang_api.save_cache_mojang_profiles(UUIDS.copy()))
loop.close()

print(UUIDS)