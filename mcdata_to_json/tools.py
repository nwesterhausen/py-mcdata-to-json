import typing
import re


def dict_merge(source: typing.Dict, destination: typing.Dict) -> typing.Dict:
    """
    run me with nosetests --with-doctest file.py

    >>> a = { 'first' : { 'all_rows' : { 'pass' : 'dog', 'number' : '1' } } }
    >>> b = { 'first' : { 'all_rows' : { 'fail' : 'cat', 'number' : '5' } } }
    >>> dict_merge(b, a) == { 'first' : { 'all_rows' : { 'pass' : 'dog', 'fail' : 'cat', 'number' : '5' } } }
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


def advancement_json_to_tree(advjson: typing.Dict) -> typing.Dict:
    tree: dict = {}
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