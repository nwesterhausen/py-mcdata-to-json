"""Methods for copying and (when neccessary) converting player data"""

import os
import nbtlib
import json
import logging
import typing

import mcdata_to_json.configuration as Config
from mcdata_to_json import LOGGER_NAME
from mcdata_to_json.tools import advancement_json_to_tree

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


def save_temp_advancement_json(uuid: str) -> None:
    filepath = os.path.join(Config.ADVANCEMENTS_DIR, "{}.json".format(uuid))
    _LOGGER.debug("Trying to open {}".format(filepath))
    with open(filepath, 'r') as af:
        parsedJson = advancement_json_to_tree(json.load(af))
        jsadv = json.dumps(parsedJson)
        with open(
                os.path.join(Config.TEMP_ADVANCEMENT_JSON_DIR,
                             "{}.json".format(uuid)), 'w') as ad:
            ad.write(jsadv)
            _LOGGER.debug("Saved parsed Advancements for {}".format(uuid))


def save_temp_stats_json(uuid: str) -> None:
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