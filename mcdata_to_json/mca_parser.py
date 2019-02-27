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

UNQUOTED_KEY_RE = re.compile("(\w+): ")
NUMBER_TYPE_RE = re.compile("([0-9.]+)(b|f|L|d|s)")
LIST_TYPE_RE = re.compile("\[(I);")


def cache_json_for_region_files():
    """Saves json for each region file into the data cache"""
    for filename in os.listdir(Config.OVERWORLD_REGION_DIR):
        cache_nbtjson_for_region(
            os.path.join(Config.OVERWORLD_REGION_DIR, filename))


def cache_nbtjson_for_region(regionfilepath):
    """Saves json for the provided region file (r.1.1.mca)"""
    region = os.path.basename(regionfilepath).replace('.mca', '')
    print(f'Working region {region}')
    mca = Mca(regionfilepath)
    nbtjson: dict = {'TileEntities': [], 'Entities': []}
    for i in range(32):
        for j in range(32):
            chunkjson = nbtjson_for_chunk(mca, i, j)
            nbtjson['TileEntities'].extend(chunkjson['TileEntities'])
            nbtjson['Entities'].extend(chunkjson['Entities'])
    save_cached_json(region, nbtjson)


def nbtjson_for_chunk(mcaobj, x, z):
    """Return json of the nbt for the chunk at x z"""
    print(f'Working chunk {x}, {z}')
    region = mcaobj.get_data(x, z)
    nbt = nbtlib.File.from_buffer(io.BytesIO(region))
    chunkjson: dict = {'TileEntities': [], 'Entities': []}
    if mcaobj.get_data_size(x, z) != 0:
        if nbt.root_name != None:
            chunkjson = recast_nbt_to_normals(nbt.root)
    return chunkjson


def save_cached_json(region, nbtjson):
    """Save compiled json of the chunks nbt to a cached file"""
    with open(os.path.join(Config.CACHED_MCA_JSON_DIR, f'{region}.json'),
              'w') as f:
        f.write(json.dumps(nbtjson))


def recast_nbt_to_normals(nbtroot: nbtlib.tag.Compound) -> dict:
    if 'Level' in nbtroot.keys():
        ents = nbtroot['Level']['Entities'].__str__()
        ents = UNQUOTED_KEY_RE.sub(r'"\1": ', ents)
        ents = NUMBER_TYPE_RE.sub(r'\1', ents)
        ents = LIST_TYPE_RE.sub(r'', ents)
        ents = ast.literal_eval(ents)
        tents = nbtroot['Level']['TileEntities'].__str__()
        # print(tents)
        tents = UNQUOTED_KEY_RE.sub(r'"\1": ', tents)
        tents = NUMBER_TYPE_RE.sub(r'\1', tents)
        tents = LIST_TYPE_RE.sub(r'[', tents)
        # print(tents)
        tents = ast.literal_eval(tents)
    else:
        ents = []
        tents = []
    return {'Entities': ents, 'TileEntities': tents}


if __name__ == '__main__':
    cache_nbtjson_for_region(
        os.path.join(Config.OVERWORLD_REGION_DIR, 'r.-1.5.mca'))
    m = Mca(os.path.join(Config.OVERWORLD_REGION_DIR, 'r.-1.-5.mca'))
    print(nbtjson_for_chunk(m, 0, 30))