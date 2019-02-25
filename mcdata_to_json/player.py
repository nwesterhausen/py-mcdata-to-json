"""Methods for copying and (when neccessary) converting player data"""

import os
import nbtlib
import json
import typing

import mcdata_to_json.configuration as Config
from mcdata_to_json.tools import advancement_json_to_tree


def save_temp_playerdata_json(uuid):
    filepath = os.path.join(Config.PLAYERDATA_DIR, "{}.dat".format(uuid))
    nbt = nbtlib.load(filepath)
    jsnbt = json.dumps(nbt[""])
    with open(
            os.path.join(Config.TEMP_PLAYERDATA_JSON_DIR,
                         "{}.json".format(uuid)), 'w') as f:
        f.write(jsnbt)


def save_temp_advancement_json(uuid: str) -> None:
    filepath = os.path.join(Config.ADVANCEMENTS_DIR, "{}.json".format(uuid))
    with open(filepath, 'r') as af:
        parsedJson = advancement_json_to_tree(json.load(af))
        jsadv = json.dumps(parsedJson)
        with open(
                os.path.join(Config.TEMP_ADVANCEMENT_JSON_DIR,
                             "{}.json".format(uuid)), 'w') as ad:
            ad.write(jsadv)


def save_temp_stats_json(uuid: str) -> None:
    filepath = os.path.join(Config.ADVANCEMENTS_DIR, "{}.json".format(uuid))
    with open(filepath, 'r') as sf:
        parsedJson = json.load(sf)
        parsedJson.pop('DataVersion', '')
        jsadv = json.dumps(parsedJson)
        with open(
                os.path.join(Config.TEMP_STATS_JSON_DIR,
                             "{}.json".format(uuid)), 'w') as ad:
            ad.write(jsadv)