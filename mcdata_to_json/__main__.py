"""Main runner"""
import logging
import os
import sys
import asyncio

from typing import List

import mcdata_to_json.configuration as Config
import mcdata_to_json.mojang_api as mojang_api
from mcdata_to_json.mcdata import data_extractor, advancements
import mcdata_to_json.player as player

Config.validatePaths()

UUIDS: List[str] = []
if (Config.PLAYERDATA_DIR not in Config.NONEXISTENT_FILES):
    UUIDS = list(
        map(lambda fn: fn.replace('.dat', ''),
            os.listdir(Config.PLAYERDATA_DIR)))

print(f'Caching json versions of all ({len(UUIDS)}) players data')
for uuid in UUIDS:
    player.save_temp_playerdata_json(uuid)
    player.save_temp_advancement_json(uuid)
    player.save_temp_stats_json(uuid)

print('Extracting possible advancements from minecraft server.jar')
data_extractor.extract_server_jar_assets()

advancements.cache_possible_advancements()
print('Exporting server advancements progress')
advancements.save_completed_advancements(UUIDS.copy())

loop = asyncio.get_event_loop()
loop.run_until_complete(mojang_api.save_cache_mojang_profiles(UUIDS.copy()))
loop.close()

print(f'Exporting combined JSON for {len(UUIDS)} players.')
list(map(player.export_player_json, UUIDS))
player.export_uuid_dict(UUIDS.copy())