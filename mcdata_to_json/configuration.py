"""Code to help create paths to all the relevant locations"""
import os
import logging
import sys

from typing import Dict, List
from argparse import ArgumentParser

from mcdata_to_json import LOGGER_NAME

_LOGGER = logging.getLogger(name=LOGGER_NAME)

parser = ArgumentParser(
    description="Python tool to create JSON files from minecraft server data.")
parser.add_argument("-c", "--config", dest="config_file",
                    help="Configuration YAML", metavar="CONFIG", default="config.yaml")
parser.add_argument("-i", "--minecraft-dir", dest="mc_dir",
                    help="Directory of the minecraft server.", metavar="MINECRAFTDIR")
parser.add_argument("-j", "--jar-name", dest="jar_name",
                    help="Name of the miencraft server jar.", metavar="SERVERJAR",
                    default="server.jar")
parser.add_argument("-o", "--outdir", dest="output_dir",
                    help="Destination directory for JSON files.", metavar="OUTPUTDIR",
                    default="./output")
parser.add_argument("-t", "--cachedir", dest="work_dir",
                    help="Destination directory for JSON files.", metavar="CACHEDIR",
                    default="./mcdata_cache")
parser.add_argument("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

args = parser.parse_args()

# Minecraft dir from config
MC_DIR = os.path.normpath(args.mc_dir) if os.path.isabs(
    args.mc_dir) else os.path.abspath(args.mc_dir)
MCJAR_FILE = os.path.join(MC_DIR, args.jar_name)  # name pulled from config

OUTPUT_DIR = os.path.normpath(args.output_dir) if os.path.isabs(
    args.output_dir) else os.path.abspath(args.output_dir)
# cache dir from config
WORK_DIR = os.path.normpath(args.work_dir) if os.path.isabs(
    args.work_dir) else os.path.abspath(args.work_dir)

## COMPUTED PATHS ##
PROPERTIES_FILE = os.path.join(MC_DIR, 'server.properties')
USERCACHE_FILE = os.path.join(MC_DIR, 'usercache.json')
OPSLIST_FILE = os.path.join(MC_DIR, 'ops.json')
LOGS_DIR = os.path.join(MC_DIR, 'logs')
WORLD_DIR = os.path.join(MC_DIR, 'world')
WORLD_DATA_DIR = os.path.join(WORLD_DIR, 'data')
DATAPACKS_DIR = os.path.join(WORLD_DIR, 'datapacks')
STATS_DIR = os.path.join(WORLD_DIR, 'stats')
ADVANCEMENTS_DIR = os.path.join(WORLD_DIR, 'advancements')
PLAYERDATA_DIR = os.path.join(WORLD_DIR, 'playerdata')
LEVELDAT_FILE = os.path.join(WORLD_DIR, 'level.dat')
OVERWORLD_REGION_DIR = os.path.join(WORLD_DIR, 'region')
NETHER_DIR = os.path.join(WORLD_DIR, 'DIM-1')
NETHER_REGION_DIR = os.path.join(NETHER_DIR, 'region')
NETHER_DATA_DIR = os.path.join(NETHER_DIR, 'data')
END_DIR = os.path.join(WORLD_DIR, 'DIM1')
END_REGION_DIR = os.path.join(END_DIR, 'region')
END_DATA_DIR = os.path.join(END_DIR, 'playerdata')
TEMP_DIR = os.path.join(WORK_DIR, '.temp')
EXTRACTED_DIR = os.path.join(WORK_DIR, 'extracted')
GENERATED_DIR = os.path.join(WORK_DIR, 'generated')
GENERATED_DATA_DIR = os.path.join(GENERATED_DIR, 'data')
EXTRACTED_DATA_DIR = os.path.join(EXTRACTED_DIR, 'data')
EXTRACTED_ASSETS_DIR = os.path.join(EXTRACTED_DIR, 'assets')
CACHED_MCA_JSON_DIR = os.path.join(WORK_DIR, 'mcajson')
TEMP_PLAYERDATA_JSON_DIR = os.path.join(TEMP_DIR, 'playerdata')
TEMP_LOG_JSON_DIR = os.path.join(TEMP_DIR, 'logs')
TEMP_ADVANCEMENT_JSON_DIR = os.path.join(TEMP_DIR, 'advancements')
TEMP_PROFILE_JSON_DIR = os.path.join(TEMP_DIR, 'profiles')

NONEXISTENT_FILES: List[str] = []


def validatePaths():
    validateDir(MC_DIR, "minecraft dir invalid", True)
    validateFile(MCJAR_FILE, "minecraft server jar doesn't exist")
    validateDir(OUTPUT_DIR, "specified output dir doesn't exist")
    validateDir(WORK_DIR, "specified cache dir doesn't exist")
    validateFile(PROPERTIES_FILE, "server.properties doesn't exist")
    validateFile(USERCACHE_FILE, "usercache.json not found")
    validateFile(OPSLIST_FILE, "ops.json not found")
    validateDir(LOGS_DIR, "logs not found in minecraft dir")
    validateDir(WORLD_DIR, "world not found in minecraft dir")
    validateDir(WORLD_DATA_DIR, "data dir not found in world dir")
    validateDir(DATAPACKS_DIR, "datapacks dir not found in world dir")
    validateDir(STATS_DIR, "stats dir not found in world dir")
    validateDir(ADVANCEMENTS_DIR, "advancements dir not found in world dir")
    validateDir(PLAYERDATA_DIR, "playerdata dir not found in world dir")
    validateFile(LEVELDAT_FILE, "level.dat not found in world dir")
    validateDir(OVERWORLD_REGION_DIR, "world region not found in world dir")
    validateDir(NETHER_DIR, "DIM-1 not found in world dir")
    validateDir(NETHER_REGION_DIR, "region not found in DIM-1")
    validateDir(NETHER_DATA_DIR, "data not found in DIM-1")
    validateDir(END_DIR, "DIM1 not found in world dir")
    validateDir(END_REGION_DIR, "region not found in DIM1")
    validateDir(END_DATA_DIR, "data not found in DIM1")
    validateDir(TEMP_DIR, "temp dir doesn't exist")
    validateDir(EXTRACTED_DIR, "extracted data dir doesn't exist")
    validateDir(GENERATED_DIR, "generated data dir doesn't exist")
    validateDir(GENERATED_DATA_DIR, "generated data dir doesn't exist")
    validateDir(EXTRACTED_DATA_DIR, "extracted data dir doesn't exist")
    validateDir(EXTRACTED_ASSETS_DIR, "extracted assets dir doesn't exist")
    validateDir(CACHED_MCA_JSON_DIR, "cached mca json file dir not found")
    validateDir(TEMP_PLAYERDATA_JSON_DIR,
                "temp playerdat json dir doesn't exist")
    validateDir(TEMP_LOG_JSON_DIR, "temp log json dir doesn't exist")
    validateDir(TEMP_ADVANCEMENT_JSON_DIR,
                "temp advancement dir doesn't exist")
    validateDir(TEMP_PROFILE_JSON_DIR, "temp profile dir doesn't exist")
    _LOGGER.debug("Non-existent files: {}".format(NONEXISTENT_FILES))


def validateFile(filepath: str, notfound_message: str, quit_on_failure=False):
    if not os.path.isfile(filepath):
        if quit_on_failure:
            _LOGGER.error("{}:{}".format(notfound_message, filepath))
            sys.exit()
        else:
            _LOGGER.warn("{}:{}".format(notfound_message, filepath))
            NONEXISTENT_FILES.append(filepath)
    else:
        _LOGGER.debug("{} is a file".format(os.path.basename(filepath)))


def validateDir(dirpath: str, notfound_message: str, quit_on_failure=False):
    if not os.path.isdir(dirpath):
        if quit_on_failure:
            _LOGGER.error("{}:{}".format(notfound_message, dirpath))
            sys.exit()
        else:
            _LOGGER.warn("{}:{}".format(notfound_message, dirpath))
            NONEXISTENT_FILES.append(dirpath)
    else:
        _LOGGER.debug("{} is a dir".format(os.path.basename(dirpath)))
