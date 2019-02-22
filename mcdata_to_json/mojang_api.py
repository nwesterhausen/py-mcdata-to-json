import re
import aiohttp
import json
import os
import logging
import base64
import time
import typing
import mcdata_to_json.configuration as Config
from mcdata_to_json import LOGGER_NAME

_LOGGER = logging.getLogger(name=LOGGER_NAME)

PROFILE_API_BASE = 'https://sessionserver.mojang.com/session/minecraft/profile'
CONSIDERED_CACHED = 1000 * 60 * 60 * 4  # 4 hours


def uri_encode_uuid(uuid: str) -> str:
    return uuid.replace('-', '')


def uri_decode_uuid(uuid: str) -> str:
    return '-'.join(
        [uuid[0, 8], uuid[8, 12], uuid[12, 16], uuid[16, 20], uuid[20]])


async def save_cache_mojang_profiles(uuids: typing.List):
    for file in os.listdir(Config.TEMP_PROFILE_JSON_DIR):
        if time.time() - os.path.getmtime(
                os.path.join(Config.TEMP_PROFILE_JSON_DIR,
                             file)) < CONSIDERED_CACHED:
            _LOGGER.info("Cached profile for {} is recent enough.".format(
                file.replace('.json', '')))
            uuids.pop(uuids.index(file.replace('.json', '')))
    # Age check here as well?
    async with aiohttp.ClientSession() as session:
        for uuid in uuids:
            profilejson = await get_mojang_profile(uuid, session)
            with open(
                    os.path.join(Config.TEMP_PROFILE_JSON_DIR,
                                 "{}.json".format(uuid)), 'w') as pf:
                pf.write(json.dumps(profilejson))


async def get_mojang_profile(uuid: str,
                             session: aiohttp.ClientSession) -> typing.Dict:
    apiTarget = "{}/{}".format(PROFILE_API_BASE, uri_encode_uuid(uuid))
    emptyResponse = {}
    async with session.get(apiTarget) as resp:
        respjson = await resp.json()
        if resp.status == 200:
            if 'error' in respjson:
                _LOGGER.warn(json.dumps(respjson))
            else:
                for property in respjson["properties"]:
                    b64_value = property["value"]
                    b64_value += "=" * ((4 - len(b64_value) % 4) % 4)
                    property["value"] = json.loads(
                        base64.decodebytes(str.encode(b64_value)))
                return respjson
        else:
            _LOGGER.warn("Unable to get profile for {} due to {}:{}".format(
                uuid, resp.status, resp.reason))
        return emptyResponse
