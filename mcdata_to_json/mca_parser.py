import io
import nbtlib
import sys
import json
import os
import ast
import re
import mcdata_to_json.configuration as Config
from mcdata_to_json.mcdata.mca_reader import Mca
from mcdata_to_json.tools import dict_merge

UNQUOTED_KEY_RE = re.compile(r"(\w+): ")
NUMBER_TYPE_RE = re.compile(r"([0-9][0-9.]*)(b|f|L|d|s|i|B)")
LIST_TYPE_RE = re.compile(r"\[(B|F|L|D|S|I);")

EMPTY_CHUNK = {
    'TileEntities': [],
    'Entities': [],
    'Timestamp': None,
    'Status': 'empty',
    'Structures': {},
    'xPos': None,
    'zPos': None,
    'InhabitedTime': None,
    'LastUpdate': None,
    'Biomes': []
}


def cache_json_for_region_files():
    """Saves json for each region file into the data cache"""
    for filename in os.listdir(Config.OVERWORLD_REGION_DIR):
        cache_nbtjson_for_region(
            os.path.join(Config.OVERWORLD_REGION_DIR, filename),
            Config.OVERWORLD_MCA_CACHE_DIR)
    print()
    print(
        f'Cached JSON for {len(os.listdir(Config.OVERWORLD_REGION_DIR))} region files in the world.'
    )
    if Config.NETHER_REGION_DIR not in Config.NONEXISTENT_FILES:
        for filename in os.listdir(Config.NETHER_REGION_DIR):
            cache_nbtjson_for_region(
                os.path.join(Config.NETHER_REGION_DIR, filename),
                Config.NETHER_MCA_CACHE_DIR)
        print()
        print(
            f'Cached JSON for {len(os.listdir(Config.NETHER_REGION_DIR))} region files in the nether.'
        )
    if Config.END_REGION_DIR not in Config.NONEXISTENT_FILES:
        for filename in os.listdir(Config.END_REGION_DIR):
            cache_nbtjson_for_region(
                os.path.join(Config.END_REGION_DIR, filename),
                Config.END_MCA_CACHE_DIR)
        print()
        print(
            f'Cached JSON for {len(os.listdir(Config.END_REGION_DIR))} region files in the nether.'
        )


def cache_nbtjson_for_region(regionfilepath: str, outputpath: str):
    """Saves json for the provided region file (r.1.1.mca)"""
    region = os.path.basename(regionfilepath).replace('.mca', '')
    cachepath = os.path.join(outputpath, f'{region}.json')
    mca = Mca(regionfilepath)
    shouldCheckCached = False
    nbtjson: dict = {'TileEntities': [], 'Entities': [], 'Chunks': {}}
    updatedChunks = 0
    if os.path.exists(cachepath) and os.path.getsize(cachepath) > 100:
        shouldCheckCached = True
        cachef = open(cachepath)
        nbtjson = json.loads(cachef.read())
        cachef.close()
    for i in range(32):
        for j in range(32):
            if shouldCheckCached and f'x{i}z{j}' in nbtjson.keys():
                if mca.get_timestamp(i,
                                     j) == nbtjson[f'x{i}z{j}']['Timestamp']:
                    sys.stdout.write(
                        '\rScanning {:10s} Cache is up to date for {:2d}, {:2d}'
                        .format(region, i, j))
                    sys.stdout.flush()
                    continue
            sys.stdout.write(
                '\rScanning {:10s} Updating chunk {:2d}, {:2d}         '.
                format(region, i, j))
            sys.stdout.flush()
            chunkjson = nbtjson_for_chunk(mca, i, j)
            updatedChunks += 1
            nbtjson['TileEntities'].extend(chunkjson['TileEntities'])
            nbtjson['Entities'].extend(chunkjson['Entities'])
            nbtjson[f'x{i}z{j}'] = {
                'Timestamp': mca.get_timestamp(i, j),
                'Status': chunkjson['Status'],
                'Structures': chunkjson['Structures'],
                'xPos': chunkjson['xPos'],
                'zPos': chunkjson['zPos'],
                'InhabitedTime': chunkjson['InhabitedTime'],
                'LastUpdate': chunkjson['LastUpdate'],
                'Biomes': chunkjson['Biomes']
            }
    save_cached_json(region, nbtjson, outputpath)
    if updatedChunks > 0:
        print()
        print(
            f'Had to update {region} cache: {updatedChunks} / {32*32} chunks.')


def nbtjson_for_chunk(mcaobj, x, z):
    """Return json of the nbt for the chunk at x z"""
    if mcaobj.get_timestamp(x, z) == 0:
        return EMPTY_CHUNK
    region = mcaobj.get_data(x, z)
    nbt = nbtlib.Compound.parse(io.BytesIO(region))
    if mcaobj.get_data_size(x, z) == 0 or len(
            nbt.keys()) == 0 or 'Level' not in nbt[""].keys():
        return EMPTY_CHUNK
    return recast_nbt_to_normals(nbt[""])


def save_cached_json(region, nbtjson, outputdir):
    """Save compiled json of the chunks nbt to a cached file"""
    with open(os.path.join(outputdir, f'{region}.json'), 'w') as f:
        f.write(json.dumps(nbtjson))


def recast_nbt_to_normals(nbtroot: nbtlib.tag.Compound) -> dict:
    level = nbtroot['Level'].__str__()
    level = UNQUOTED_KEY_RE.sub(r'"\1": ', level)
    level = NUMBER_TYPE_RE.sub(r'\1', level)
    level = LIST_TYPE_RE.sub(r'[', level)
    level = ast.literal_eval(level)
    if 'Status' not in level.keys():
        level['Status'] = 'unknown'
    if 'Structures' not in level.keys():
        level['Structures'] = {}
    return {
        'xPos': level['xPos'],
        'zPos': level['zPos'],
        'InhabitedTime': level['InhabitedTime'],
        'LastUpdate': level['LastUpdate'],
        'Biomes': level['Biomes'],
        'Status': level['Status'],
        'Structures': level['Structures'],
        'Entities': level['Entities'],
        'TileEntities': level['TileEntities']
    }


if __name__ == '__main__':
    Config.validatePaths()
    cache_nbtjson_for_region(
        os.path.join(Config.OVERWORLD_REGION_DIR, 'r.4.-1.mca'),
        Config.OVERWORLD_MCA_CACHE_DIR)
    # m = Mca(os.path.join(Config.OVERWORLD_REGION_DIR, 'r.4.-1.mca'))
    # print(nbtjson_for_chunk(m, 0, 3))
