"""Methods for copying and (when neccessary) converting player data"""

import os
import nbtlib
import json
import typing

import mcdata_to_json.configuration as Config
from mcdata_to_json.tools import advancement_json_to_tree, dict_merge


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


def export_player_json(uuid: str) -> None:
    combined = get_combined_player_dict(uuid)
    with open(os.path.join(Config.OUTPUT_DIR, f'{uuid}.json'), 'w') as f:
        f.write(json.dumps(combined))


def get_combined_player_dict(uuid: str) -> dict:
    combined: dict = {}
    with open(os.path.join(Config.TEMP_ADVANCEMENT_JSON_DIR,
                           f'{uuid}.json')) as f:
        combined['advancements'] = json.loads(f.read())
    with open(os.path.join(Config.TEMP_PLAYERDATA_JSON_DIR,
                           f'{uuid}.json')) as f:
        combined['data'] = json.loads(f.read())
    with open(os.path.join(Config.TEMP_PROFILE_JSON_DIR, f'{uuid}.json')) as f:
        dict_merge(json.loads(f.read()), combined)
    with open(os.path.join(Config.TEMP_STATS_JSON_DIR, f'{uuid}.json')) as f:
        combined['stats'] = json.loads(f.read())
    return combined


def get_uuid_dict(uuids: list) -> dict:
    iddict: dict = {}
    for uuid in uuids:
        with open(os.path.join(Config.TEMP_PROFILE_JSON_DIR,
                               f'{uuid}.json')) as f:
            iddict[uuid] = json.loads(f.read())['name']
    return iddict


def export_uuid_dict(uuids: list) -> None:
    iddict: dict = get_uuid_dict(uuids)
    with open(os.path.join(Config.OUTPUT_DIR, 'uuids.json'), 'w') as f:
        f.write(json.dumps(iddict))
