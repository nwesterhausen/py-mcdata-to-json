"""Code to parse player advancements"""

import os
import json
import logging
import typing
import re

import mcdata_to_json.configuration as Config
from mcdata_to_json.tools import dict_merge
from mcdata_to_json import LOGGER_NAME

_LOGGER = logging.getLogger(name=LOGGER_NAME)


def save_temp_advancement_json(uuid: str) -> typing.Dict:
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


def advancement_json_to_tree(advjson: typing.Dict) -> typing.Dict:
    tree = {}
    for key, value in advjson.items():
        dict_merge(dict_from_advancement_entry(key, value), tree)
    tree.pop('DataVersion', None)
    return tree


def dict_from_advancement_entry(advkey: str,
                                advvalue: typing.Dict) -> typing.Dict:
    patharr = re.split('/|:', advkey)
    return dict_from_path(patharr, advvalue)


def dict_from_path(patharr: typing.List, endvalue: typing.Dict) -> typing.Dict:
    if len(patharr) == 1:
        return {patharr[0]: endvalue}
    else:
        return {patharr[0]: dict_from_path(patharr[1:], endvalue)}