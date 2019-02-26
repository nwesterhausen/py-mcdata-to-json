"""Code to read and understand level.dat"""
import nbtlib
import os
import json
import mcdata_to_json.configuration as Config


def export_level_dat() -> None:
    nbt = nbtlib.load(Config.LEVELDAT_FILE)
    jsnbt = json.dumps(nbt[""])
    with open(os.path.join(Config.OUTPUT_DIR, "leveldat.json"), 'w') as f:
        f.write(jsnbt)


def export_raids_dat() -> None:
    raidsJson: dict = {}
    nbt = nbtlib.load(os.path.join(Config.WORLD_DATA_DIR, 'raids.dat'))
    raidsJson['overworld'] = nbt[""]
    nbt = nbtlib.load(os.path.join(Config.NETHER_DATA_DIR, 'raids_nether.dat'))
    raidsJson['nether'] = nbt[""]
    nbt = nbtlib.load(os.path.join(Config.END_DATA_DIR, 'raids_end.dat'))
    raidsJson['end'] = nbt[""]
    with open(os.path.join(Config.OUTPUT_DIR, 'raids.json'), 'w') as f:
        f.write(json.dumps(raidsJson))


def export_scoreboard_dat() -> None:
    nbt = nbtlib.load(os.path.join(Config.WORLD_DATA_DIR, 'scoreboard.dat'))
    jsnbt = json.dumps(nbt[""])
    with open(os.path.join(Config.OUTPUT_DIR, "scoreboard.json"), 'w') as f:
        f.write(jsnbt)


def export_villages_dat() -> None:
    villagesJson: dict = {}
    nbt = nbtlib.load(os.path.join(Config.WORLD_DATA_DIR, 'villages.dat'))
    villagesJson['overworld'] = nbt[""]
    nbt = nbtlib.load(
        os.path.join(Config.WORLD_DATA_DIR, 'villages_nether.dat'))
    villagesJson['nether'] = nbt[""]
    nbt = nbtlib.load(os.path.join(Config.WORLD_DATA_DIR, 'villages_end.dat'))
    villagesJson['end'] = nbt[""]
    with open(os.path.join(Config.OUTPUT_DIR, 'villages.json'), 'w') as f:
        f.write(json.dumps(villagesJson))
