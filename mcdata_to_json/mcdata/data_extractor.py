"""Code to extract advancements and other data from minecraft server jar"""
import zipfile
import os
import typing

import mcdata_to_json.configuration as Config


def extract_server_jar_assets() -> None:
    if Config.MCJAR_FILE in Config.NONEXISTENT_FILES:
        return
    with zipfile.ZipFile(Config.MCJAR_FILE, 'r') as jar:
        print("Extracting {} files from {} data/".format(
            count_names_start_with('data/', jar.namelist()),
            os.path.basename(Config.MCJAR_FILE)))
        print("Extracting {} files from {}  assets/".format(
            count_names_start_with('assets/', jar.namelist()),
            os.path.basename(Config.MCJAR_FILE)))
        for piece in jar.namelist():
            # We just trust that any existing file is one we put there.
            if not os.path.exists(os.path.join(Config.EXTRACTED_DIR, piece)):
                if piece.startswith('data/'):
                    jar.extract(piece, Config.EXTRACTED_DIR)
                elif piece.startswith('assets/'):
                    jar.extract(piece, Config.EXTRACTED_DIR)


def count_names_start_with(startwith: str, namelist: typing.List) -> int:
    return len(list(filter(lambda l: l.startswith(startwith), namelist)))


# When we extract this stuff, we kinda just want it all mushed together.
def extract_datapack(datapackPath: str) -> None:
    with zipfile.ZipFile(datapackPath) as pack:
        print("Extracting {} files from {}".format(
            len(pack.namelist()), os.path.basename(datapackPath)))
        pack.extractall(Config.EXTRACTED_DIR)