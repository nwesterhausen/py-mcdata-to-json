"""Parse the possible advancements"""
import os
import typing
import json

import mcdata_to_json.configuration as Config


def cache_possible_advancements() -> None:
    advancementsList = create_advancement_dictionary_from_filestructure(
        Config.EXTRACTED_DATA_DIR)
    with open(
            os.path.join(Config.TEMP_DIR, 'possible_advancements.json'),
            'w') as f:
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


if __name__ == '__main__':
    cache_possible_advancements()