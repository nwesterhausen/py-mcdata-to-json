import re
import aiohttp
import json
import os
import logging
import base64
import time
import typing
import mcdata_to_json.configuration as Config
import mcdata_to_json.error_handling as errors

PROFILE_API_BASE = 'https://sessionserver.mojang.com/session/minecraft/profile'
CONSIDERED_CACHED = 1000 * 60 * 60 * 4  # 4 hours


def uri_encode_uuid(uuid: str) -> str:
    return uuid.replace('-', '')


def uri_decode_uuid(uuid: str) -> str:
    return '-'.join([
        uuid[slice(0, 8)], uuid[slice(8, 12)], uuid[slice(12, 16)], uuid[slice(
            16, 20)], uuid[slice(20)]
    ])


async def save_cache_mojang_profiles(uuids: typing.List) -> None:
    for file in os.listdir(Config.TEMP_PROFILE_JSON_DIR):
        if time.time() - os.path.getmtime(
                os.path.join(Config.TEMP_PROFILE_JSON_DIR,
                             file)) < CONSIDERED_CACHED:
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
    emptyResponse: dict = {}
    async with session.get(apiTarget) as resp:
        respjson = await resp.json()
        if resp.status == 200:
            if 'error' in respjson:
                errors.InvalidQueryError(json.dumps(respjson))
            else:
                for property in respjson["properties"]:
                    b64_value = property["value"]
                    b64_value += "=" * ((4 - len(b64_value) % 4) % 4)
                    property["value"] = json.loads(
                        base64.decodebytes(str.encode(b64_value)))
                return respjson
        else:
            errors.Non200ResponseError(
                "Unable to get profile for {} due to {}:{}".format(
                    uuid, resp.status, resp.reason))
        return emptyResponse
