"""Parse the possible advancements"""
import os
import typing
import json

import mcdata_to_json.configuration as Config

POSSIBLE_ADVANCEMENTS_FILE = os.path.join(Config.TEMP_DIR,
                                          'possible_advancements.json')
COMPLETED_ADVANCEMENTS_FILE = os.path.join(Config.OUTPUT_DIR,
                                           'server_advancements.json')


def save_completed_advancements(uuids: list) -> None:
    """Read through player advancements and note progress at server level"""
    # First read possible advancements
    serverAdvancements: dict = {}
    with open(POSSIBLE_ADVANCEMENTS_FILE, 'r') as f:
        serverAdvancements = json.loads(f.read())
    # Then read player-by-player
    for uuid in uuids:
        f = open(
            os.path.join(Config.TEMP_ADVANCEMENT_JSON_DIR, f"{uuid}.json"))
        serverAdvancements = fillin_completed_advancements(
            serverAdvancements, uuid, json.loads(f.read()))
    # Last write advancements progress
    with open(COMPLETED_ADVANCEMENTS_FILE, 'w') as f:
        f.write(json.dumps(serverAdvancements))


def fillin_completed_advancements(
        possibleAdvancements: dict, uuid: str,
        playerCompletedAdvancements: dict) -> typing.Dict:
    """Mark the completed player advancements in possible advancements"""
    for domain in possibleAdvancements:
        for category in possibleAdvancements[domain]:
            if category in playerCompletedAdvancements[domain]:
                for advancement in possibleAdvancements[domain][category]:
                    if advancement in playerCompletedAdvancements[domain][
                            category]:
                        possibleAdvancements[domain][category][
                            advancement] = mark_if_advancement_completed(
                                possibleAdvancements[domain][category]
                                [advancement],
                                playerCompletedAdvancements[domain][category]
                                [advancement], uuid)

    return possibleAdvancements


def mark_if_advancement_completed(serverAdvancement: dict,
                                  playerAdvancement: dict, uuid: str) -> dict:
    if playerAdvancement['done']:
        serverAdvancement['completed'].append(uuid)
    for critereon in serverAdvancement['criteria']:
        if critereon in playerAdvancement['criteria']:
            serverAdvancement['criteria'][critereon]['completed'].append(uuid)
    return serverAdvancement


def cache_possible_advancements() -> None:
    advancementsList = create_advancement_dictionary_from_filestructure(
        Config.EXTRACTED_DATA_DIR)
    with open(POSSIBLE_ADVANCEMENTS_FILE, 'w') as f:
        f.write(json.dumps(advancementsList))


def create_advancement_dictionary_from_filestructure(
        containingPath: str) -> typing.Dict:
    advDict: dict = {}
    domains = os.listdir(containingPath)
    for domain in domains:
        if os.path.isdir(os.path.join(containingPath, domain)):
            if domain not in advDict:
                advDict[domain] = {}
            add_categories_to_domain(
                advDict[domain],
                os.path.join(containingPath, domain, 'advancements'))
    return advDict


def add_categories_to_domain(domainDict: typing.Dict,
                             categoriesParentDir: str) -> None:
    categories = os.listdir(categoriesParentDir)
    for category in categories:
        if os.path.isdir(os.path.join(categoriesParentDir, category)):
            if category not in domainDict:
                domainDict[category] = {}
            add_advancements_to_category(
                domainDict[category],
                os.path.join(categoriesParentDir, category))


def add_advancements_to_category(categorydict: typing.Dict,
                                 advancementParentDir: str) -> None:
    advancements = os.listdir(advancementParentDir)
    for advancement in advancements:
        if advancement.endswith('.json'):
            categorydict[advancement.replace(
                '.json', '')] = get_dict_from_advancement_json(
                    os.path.join(advancementParentDir, advancement))


def get_dict_from_advancement_json(advancementpath: str) -> typing.Dict:
    with open(advancementpath, 'r') as f:
        advdict = json.loads(f.read())
        for critereon in advdict['criteria']:
            advdict['criteria'][critereon]['completed'] = []
        advdict['completed'] = []
        return advdict
