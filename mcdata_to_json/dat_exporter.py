"""Code to read and understand level.dat"""
import nbtlib
import os
import json
import mcdata_to_json.configuration as Config


def export_level_dat() -> None:
    nbt = nbtlib.load(Config.LEVELDAT_FILE)
    jsnbt = json.dumps(nbt)
    with open(os.path.join(Config.OUTPUT_DIR, "leveldat.json"), 'w') as f:
        f.write(jsnbt)


def export_raids_dat() -> None:
    raidsJson: dict = {}
    if (Config.OVERWORLD_RAIDS_FILE not in Config.NONEXISTENT_FILES):
        nbt = nbtlib.load(Config.OVERWORLD_RAIDS_FILE)
        raidsJson['overworld'] = nbt
    if (Config.NETHER_RAIDS_FILE not in Config.NONEXISTENT_FILES):
        nbt = nbtlib.load(Config.NETHER_RAIDS_FILE)
        raidsJson['nether'] = nbt
    if (Config.END_RAIDS_FILE not in Config.NONEXISTENT_FILES):
        nbt = nbtlib.load(Config.END_RAIDS_FILE)
        raidsJson['end'] = nbt
    with open(os.path.join(Config.OUTPUT_DIR, 'raids.json'), 'w') as f:
        f.write(json.dumps(raidsJson))


def export_scoreboard_dat() -> None:
    scoreboardJson: dict = {}
    if (Config.SCOREBOARDDAT_FILE not in Config.NONEXISTENT_FILES):
        nbt = nbtlib.load(os.path.join(Config.SCOREBOARDDAT_FILE))
        scoreboardJson = nbt
    with open(os.path.join(Config.OUTPUT_DIR, "scoreboard.json"), 'w') as f:
        f.write(json.dumps(scoreboardJson))


def export_villages_dat() -> None:
    villagesJson: dict = {}
    if (Config.OVERWORLD_VILLAGE_FILE not in Config.NONEXISTENT_FILES):
        nbt = nbtlib.load(Config.OVERWORLD_VILLAGE_FILE)
        villagesJson['overworld'] = nbt
    if (Config.NETHER_VILLAGE_FILE not in Config.NONEXISTENT_FILES):
        nbt = nbtlib.load(Config.NETHER_VILLAGE_FILE)
        villagesJson['nether'] = nbt
    if (Config.END_VILLAGE_FILE not in Config.NONEXISTENT_FILES):
        nbt = nbtlib.load(Config.END_VILLAGE_FILE)
        villagesJson['end'] = nbt
    with open(os.path.join(Config.OUTPUT_DIR, 'villages.json'), 'w') as f:
        f.write(json.dumps(villagesJson))
