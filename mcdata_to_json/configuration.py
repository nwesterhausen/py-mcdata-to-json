"""Code to help create paths to all the relevant locations"""
import os
import logging
import sys
import typing
import mcdata_to_json.error_handling as errors

from argparse import ArgumentParser

parser = ArgumentParser(
    description="Python tool to create JSON files from minecraft server data.")
parser.add_argument(
    "-c",
    "--config",
    dest="config_file",
    help="Configuration YAML",
    metavar="CONFIG",
    default="config.yaml")
parser.add_argument(
    "-i",
    "--minecraft-dir",
    dest="mc_dir",
    help="Directory of the minecraft server.",
    metavar="MINECRAFTDIR")
parser.add_argument(
    "-j",
    "--jar-name",
    dest="jar_name",
    help="Name of the miencraft server jar.",
    metavar="SERVERJAR",
    default="server.jar")
parser.add_argument(
    "-o",
    "--outdir",
    dest="output_dir",
    help="Destination directory for JSON files.",
    metavar="OUTPUTDIR",
    default="./output")
parser.add_argument(
    "-t",
    "--cachedir",
    dest="work_dir",
    help="Destination directory for JSON files.",
    metavar="CACHEDIR",
    default="./mcdata_cache")

args = parser.parse_args()

# Minecraft dir from config
MC_DIR: str = os.path.normpath(args.mc_dir) if os.path.isabs(
    args.mc_dir) else os.path.abspath(args.mc_dir)
MCJAR_FILE: str = os.path.join(MC_DIR,
                               args.jar_name)  # name pulled from config

OUTPUT_DIR: str = os.path.normpath(args.output_dir) if os.path.isabs(
    args.output_dir) else os.path.abspath(args.output_dir)
# cache dir from config
WORK_DIR: str = os.path.normpath(args.work_dir) if os.path.isabs(
    args.work_dir) else os.path.abspath(args.work_dir)

## COMPUTED PATHS ##
PROPERTIES_FILE: str = os.path.join(MC_DIR, 'server.properties')
USERCACHE_FILE: str = os.path.join(MC_DIR, 'usercache.json')
OPSLIST_FILE: str = os.path.join(MC_DIR, 'ops.json')
LOGS_DIR: str = os.path.join(MC_DIR, 'logs')
WORLD_DIR: str = os.path.join(MC_DIR, 'world')
WORLD_DATA_DIR: str = os.path.join(WORLD_DIR, 'data')
DATAPACKS_DIR: str = os.path.join(WORLD_DIR, 'datapacks')
STATS_DIR: str = os.path.join(WORLD_DIR, 'stats')
ADVANCEMENTS_DIR: str = os.path.join(WORLD_DIR, 'advancements')
PLAYERDATA_DIR: str = os.path.join(WORLD_DIR, 'playerdata')
LEVELDAT_FILE: str = os.path.join(WORLD_DIR, 'level.dat')
OVERWORLD_REGION_DIR: str = os.path.join(WORLD_DIR, 'region')
NETHER_DIR: str = os.path.join(WORLD_DIR, 'DIM-1')
NETHER_REGION_DIR: str = os.path.join(NETHER_DIR, 'region')
NETHER_DATA_DIR: str = os.path.join(NETHER_DIR, 'data')
END_DIR: str = os.path.join(WORLD_DIR, 'DIM1')
END_REGION_DIR: str = os.path.join(END_DIR, 'region')
END_DATA_DIR: str = os.path.join(END_DIR, 'data')
TEMP_DIR: str = os.path.join(WORK_DIR, '.temp')
EXTRACTED_DIR: str = os.path.join(WORK_DIR, 'extracted')
GENERATED_DIR: str = os.path.join(WORK_DIR, 'generated')
GENERATED_DATA_DIR: str = os.path.join(GENERATED_DIR, 'data')
EXTRACTED_DATA_DIR: str = os.path.join(EXTRACTED_DIR, 'data')
EXTRACTED_ASSETS_DIR: str = os.path.join(EXTRACTED_DIR, 'assets')
CACHED_MCA_JSON_DIR: str = os.path.join(WORK_DIR, 'mcajson')
OVERWORLD_MCA_CACHE_DIR: str = os.path.join(CACHED_MCA_JSON_DIR, 'world')
NETHER_MCA_CACHE_DIR: str = os.path.join(CACHED_MCA_JSON_DIR, 'nether')
END_MCA_CACHE_DIR: str = os.path.join(CACHED_MCA_JSON_DIR, 'end')
TEMP_PLAYERDATA_JSON_DIR: str = os.path.join(TEMP_DIR, 'playerdata')
TEMP_LOG_JSON_DIR: str = os.path.join(TEMP_DIR, 'logs')
TEMP_ADVANCEMENT_JSON_DIR: str = os.path.join(TEMP_DIR, 'advancements')
TEMP_PROFILE_JSON_DIR: str = os.path.join(TEMP_DIR, 'profiles')
TEMP_STATS_JSON_DIR: str = os.path.join(TEMP_DIR, 'stats')

NONEXISTENT_FILES: typing.List[str] = []


def validatePaths() -> None:
    validateDir(MC_DIR, "minecraft dir invalid", raise_on_failure=True)
    validateFile(MCJAR_FILE, "minecraft server jar")
    validateDir(
        OUTPUT_DIR, "specified output dir", create_dir_if_not_exists=True)
    validateDir(WORK_DIR, "specified cache dir", create_dir_if_not_exists=True)
    validateFile(PROPERTIES_FILE, "server.properties")
    validateFile(USERCACHE_FILE, "usercache.json ")
    validateFile(OPSLIST_FILE, "ops.json ")
    validateDir(LOGS_DIR, "logs")
    validateDir(WORLD_DIR, "world")
    validateDir(WORLD_DATA_DIR, "data dir")
    validateDir(DATAPACKS_DIR, "datapacks dir")
    validateDir(STATS_DIR, "stats dir")
    validateDir(ADVANCEMENTS_DIR, "advancements dir")
    validateDir(PLAYERDATA_DIR, "playerdata dir")
    validateFile(LEVELDAT_FILE, "level.dat")
    validateDir(OVERWORLD_REGION_DIR, "world region")
    validateDir(NETHER_DIR, "DIM-1")
    validateDir(NETHER_REGION_DIR, "region")
    validateDir(NETHER_DATA_DIR, "data")
    validateDir(END_DIR, "DIM1")
    validateDir(END_REGION_DIR, "region")
    validateDir(END_DATA_DIR, "data")
    validateDir(TEMP_DIR, "temp dir", create_dir_if_not_exists=True)
    validateDir(
        EXTRACTED_DIR, "extracted data dir", create_dir_if_not_exists=True)
    validateDir(
        GENERATED_DIR, "generated data dir", create_dir_if_not_exists=True)
    validateDir(
        GENERATED_DATA_DIR,
        "generated data dir",
        create_dir_if_not_exists=True)
    validateDir(
        EXTRACTED_DATA_DIR,
        "extracted data dir",
        create_dir_if_not_exists=True)
    validateDir(
        EXTRACTED_ASSETS_DIR,
        "extracted assets dir",
        create_dir_if_not_exists=True)
    validateDir(
        CACHED_MCA_JSON_DIR,
        "cached mca json file dir ",
        create_dir_if_not_exists=True)
    validateDir(
        OVERWORLD_MCA_CACHE_DIR,
        "cached mca json file dir ",
        create_dir_if_not_exists=True)
    validateDir(
        NETHER_MCA_CACHE_DIR,
        "cached mca json file dir ",
        create_dir_if_not_exists=True)
    validateDir(
        END_MCA_CACHE_DIR,
        "cached mca json file dir ",
        create_dir_if_not_exists=True)
    validateDir(
        TEMP_PLAYERDATA_JSON_DIR,
        "temp playerdat json dir",
        create_dir_if_not_exists=True)
    validateDir(
        TEMP_LOG_JSON_DIR, "temp log json dir", create_dir_if_not_exists=True)
    validateDir(
        TEMP_ADVANCEMENT_JSON_DIR,
        "temp advancement dir",
        create_dir_if_not_exists=True)
    validateDir(
        TEMP_PROFILE_JSON_DIR,
        "temp profile dir",
        create_dir_if_not_exists=True)
    validateDir(
        TEMP_STATS_JSON_DIR, "temp stats dir", create_dir_if_not_exists=True)


def validateFile(filepath: str, notfound_message: str,
                 raise_on_failure=False) -> None:
    if not os.path.isfile(filepath):
        if raise_on_failure:
            raise errors.MissingRequiredFileError("File : {}. ({})".format(
                filepath, notfound_message))
        else:
            NONEXISTENT_FILES.append(filepath)


def validateDir(dirpath: str,
                notfound_message: str,
                raise_on_failure=False,
                create_dir_if_not_exists=False) -> None:
    if not os.path.isdir(dirpath):
        if raise_on_failure:
            raise errors.MissingRequiredFileError("Dir : {} ({})".format(
                dirpath,
                notfound_message,
            ))
        elif create_dir_if_not_exists:
            os.mkdir(dirpath)
        else:
            NONEXISTENT_FILES.append(dirpath)
