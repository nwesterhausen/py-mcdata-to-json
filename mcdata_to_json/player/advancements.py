"""Code to parse player advancements"""

import os
import re
import json
import logging
from typing import Dict, List

import mcdata_to_json.configuration as Config
from mcdata_to_json import LOGGER_NAME

_LOGGER = logging.getLogger(name=LOGGER_NAME)


def save_temp_advancement_json(uuid: str) -> Dict:
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


def advancement_json_to_tree(advjson: Dict) -> Dict:
    tree = {}
    for key, value in advjson.items():
        dict_merge(dict_from_advancement_entry(key, value), tree)
    tree.pop('DataVersion', None)
    return tree


def dict_from_advancement_entry(advkey: str, advvalue: Dict) -> Dict:
    patharr = re.split('/|:', advkey)
    return dict_from_path(patharr, advvalue)


def dict_from_path(patharr: List, endvalue: Dict) -> Dict:
    if len(patharr) == 1:
        return {patharr[0]: endvalue}
    else:
        return {patharr[0]: dict_from_path(patharr[1:], endvalue)}


def dict_merge(source, destination):
    """
    run me with nosetests --with-doctest file.py

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
    True
    """
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            dict_merge(value, node)
        else:
            destination[key] = value

    return destination