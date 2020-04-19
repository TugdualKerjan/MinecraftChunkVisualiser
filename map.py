#!/usr/bin/env python
"""
Finds the contents of the different blocks in a level, taking different data values (sub block types) into account.
"""

import json
import locale
import os
import sys
import pprint
1

# local module
try:
    import nbt
except ImportError:
    # nbt not in search path. Let's see if it can be found in the parent folder
    extrasearchpath = os.path.realpath(
        os.path.join(__file__, os.pardir, os.pardir))
    if not os.path.exists(os.path.join(extrasearchpath, 'nbt')):
        raise
    sys.path.append(extrasearchpath)

block_colors = {
    # 'acacia_leaves':        [114, 64,  22],
    # 'acacia_log':           [35,  93,  30],
    # 'air':                  [60, 100, 90],
    'andesite':             [0,   0,   32],
    'azure_bluet':          [0,   0,   100],
    'bedrock':              [0,   0,   10],
    # 'birch_leaves':         [114, 64,  22],
    # 'birch_log':            [35,  93,  30],
    'blue_orchid':          [0,   0,   100],
    'bookshelf':            [0,   0,   100],
    'brown_mushroom':       [0,   0,   100],
    'brown_mushroom_block': [0,   0,   100],
    'cactus':               [126, 61,  20],
    'chest':                [0,   100, 50],
    # 'clay':                 [7,   62,  23],
    'coal_ore':             [0,   0,   10],
    'cobblestone':          [0,   0,   25],
    'cobblestone_stairs':   [0,   0,   25],
    'crafting_table':       [0,   0,   100],
    'dandelion':            [60,  100, 60],
    # 'dark_oak_leaves':      [114, 64,  22],
    # 'dark_oak_log':         [35,  93,  30],
    'dark_oak_planks':      [35,  93,  30],
    'dead_bush':            [0,   0,   100],
    'diorite':              [0,   0,   32],
    'dirt':                 [27,  51,  15],
    'end_portal_frame':     [0,   100, 50],
    'farmland':             [35,  93,  15],
    'fire':                 [55,  100, 50],
    'flowing_lava':         [16,  100, 48],
    'flowing_water':        [228, 50,  23],
    'glass_pane':           [0,   0,   100],
    'granite':              [0,   0,   32],
    'grass':                [94,  42,  25],
    'grass_block':          [94,  42,  32],
    'gravel':               [21,  18,  20],
    'ice':                  [240, 10,  95],
    'infested_stone':       [0, 0, 32],
    'iron_ore':             [0,  10,  61],
    'iron_bars':            [22,  65,  61],
    'ladder':               [35,  93,  30],
    'lava':                 [16,  100, 48],
    'lilac':                [0,   0,   100],
    'lily_pad':             [114, 64,  18],
    'lit_pumpkin':          [24,  100, 45],
    'mossy_cobblestone':    [115, 30,  50],
    'mushroom_stem':        [0,   0,   100],
    'oak_door':             [35,  93,  30],
    'oak_fence':            [35,  93,  30],
    'oak_fence_gate':       [35,  93,  30],
    # 'oak_leaves':           [114, 64,  22],
    # 'oak_log':              [35,  93,  30],
    'oak_planks':           [35,  93,  30],
    'oak_pressure_plate':   [35,  93,  30],
    'oak_stairs':           [114, 64,  22],
    'peony':                [0,   0,   100],
    'pink_tulip':           [0,   0,   0],
    'poppy':                [0,   100, 50],
    'pumpkin':              [24,  100, 45],
    'rail':                 [33,  81,  50],
    # 'red_mushroom':         [0,   50,  20],
    # 'red_mushroom_block':   [0,   50,  20],
    'rose_bush':            [0,   0,   100],
    'sugar_cane':           [123, 70,  50],
    'sand':                 [53,  22,  58],
    'sandstone':            [48,  31,  40],
    'seagrass':             [94,  42,  25],
    'sign':                 [114, 64,  22],
    # 'spruce_leaves':        [114, 64,  22],
    # 'spruce_log':           [35,  93,  30],
    'stone':                [0,   0,   32],
    'stone_slab':           [0,   0,   32],
    'tall_grass':           [94,  42,  25],
    'tall_seagrass':        [94,  42,  25],
    'torch':                [60,  100, 50],
    'snow':                 [240, 10,  85],
    'spawner':              [180, 100, 50],
    'vine':                 [114, 64,  18],
    'wall_torch':           [60,  100, 50],
    'water':                [228, 50,  23],
    'wheat':                [123, 60,  50],
    'white_wool':           [0,   0,   100]
}

row = [None]*512*512

def blocks_to_color_for_a_chunk(chunk: AnvilChunk):
    for y in range(256):
        for z in range(16):
            for x in range(16):
                # if(x == 0 or x == 15 or z == 0 or z == 15):
                block_id = chunk.get_block(x, y, z)
                if block_id in block_colors:
                    color = block_colors[block_id]
                    row.insert(x + z * 16 + y * 256, color)
    for z in range(16):
        for x in range(16):
            y = 255
            while y > 0:
                block_id = chunk.get_block(x, y, z)
                if block_id in block_colors:
                    print("Index : " + str(x + z * 16) + " " + str(block_id))
                    color = block_colors[block_id]
                    row[x + z * 16 + y * 256] = color
                    y = 0
                else:
                    y -= 1


def heighest_blocks_in_chunk(chunk: AnvilChunk):
    cx, cz = chunk.get_coords()
    for z in range(16):
        for x in range(16):
            y = 255
            while y > 0:
                block_id = chunk.get_block(x, y, z)
                if block_id in block_colors:
                    
                    # print("Index : " + str(x + z * 16) + " " + str(block_id))
                    color = block_colors[block_id].copy()
                    color.insert(3, y)
                    row[x + z * 16 + cx*16*16 + cz*16*16*32] = color
                    y = 0
                else:
                    y -= 1


def process_region_file(region: RegionFile):
    for chunk in region.iter_chunks():
        print(AnvilChunk(chunk).get_coords())
        heighest_blocks_in_chunk(AnvilChunk(chunk))


def print_results():
    with open("data.json", 'w') as outfile:
        json.dump(row, outfile)


def main(world_folder):
    world = WorldFolder(world_folder)

    try:
        region = world.get_region(0, 0)
        process_region_file(region)
        print_results()

    except KeyboardInterrupt:
        print('Keyboard interrupt!')
        print_results()
        return 75  # EX_TEMPFAIL

    return 0  # EX_OK


if __name__ == '__main__':
    world_folder = "/home/tugdual/snap/mc-installer/496/.minecraft/saves/World/"
    # clean path name, eliminate trailing slashes. required for os.path.basename()
    world_folder = os.path.normpath(world_folder)
    if (not os.path.exists(world_folder)):
        print("No such folder as " + world_folder)
        sys.exit(72)  # EX_IOERR
    start, stop = None, None

    sys.exit(main(world_folder))
