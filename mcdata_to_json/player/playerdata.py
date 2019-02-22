"""Code to read and parse playerdata.dat files"""
import nbtlib
import os
import json
import logging

import mcdata_to_json.configuration as Config
from mcdata_to_json import LOGGER_NAME

_LOGGER = logging.getLogger(name=LOGGER_NAME)


def save_temp_playerdata_json(uuid):
    filepath = os.path.join(Config.PLAYERDATA_DIR, "{}.dat".format(uuid))
    _LOGGER.debug("Trying to open {}".format(filepath))
    nbt = nbtlib.load(filepath)
    jsnbt = json.dumps(nbt[""])
    with open(
            os.path.join(Config.TEMP_PLAYERDATA_JSON_DIR,
                         "{}.json".format(uuid)), 'w') as f:
        f.write(jsnbt)
        _LOGGER.debug("Saved parsed player.dat for {}".format(uuid))
