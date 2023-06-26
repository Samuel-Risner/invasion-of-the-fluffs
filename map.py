""" How maps are build (in the json files):
The tiles are isometric, now if you imagine rotating them to the right by 45° you get normal squares:

    /\ -> 45° ->  _
    \/           |_|

In the file there is a list containing different building parts:
    [int, int, bool, bool]
        -> the first integer define the contents for the tile:
            -1 -> nothing
            0 -> tree
            1 -> rock
            2 -> pond

            3 -> brain  ########################################
            4 -> fluff
            5 -> chest
            6 -> relic
            7 -> story
            8 -> read story
        -> the second int defines the tile type
            0 -> barren
            1 -> grass
            2 -> rock
            3 -> water shallow
            4 -> water solid
        -> 1. bool
            If the tile is to be drawn to the canvas
        -> 2. bool
            If the player has already been on the tile
    [int, int, bool, bool, bool]
        -> the first 4 values are the same as above
        -> last bool (or anything)
            Indicates that the player spawns/respawn there
            The actual value of the bool is irrelevant
    [int]
        -> 0
            A new line starts
            Since isometric tiles are not like a normal grid:
                 _ _ _
                |_|_|_|
                |_|_|_|
                |_|_|_|

            But more like this:

                /\/\/\/\/\/\/\.
                \/\/\/\/\/\/\/\.
                 \/\/\/\/\/\/\/\.
                  \/\/\/\/\/\/\/\.
                   \/\/\/\/\/\/\/\.
                    \/\/\/\/\/\/\/\.

            The tiles are added on different sides each time:

                /\/\/\/\/\/\/\/.
                \/\/\/\/\/\/\/\.
                /\/\/\/\/\/\/\/.
                \/\/\/\/\/\/\/\.
                /\/\/\/\/\/\/\/.
                \/\/\/\/\/\/\/\.
        -> 1 
            empty
"""

import json

from tile import Tile
from asset_handler import AssetHandler
from settings import TILES_WIDTH, TILES_HEIGHT_SMALL
from tile_stopper import TileStopper
from mobs import Brain, Fluff, Chest, Relic

def load_map(map_name:str, asset_handler:AssetHandler) -> \
    tuple[list[Tile], Tile, list[Brain], list[Fluff], list[Chest], list[Relic]]:
    """`@param map_name` also includes the path (not the file extension), so that save games can also be loaded."""
    
    """Load contents from file."""
    with open(f"{map_name}.json", "r") as d:
        content = json.load(d)

    tiles = []
    next_x = [0, TILES_WIDTH / 2]
    x, y = next_x[0], 0
    x_add = TILES_WIDTH
    y_add = TILES_HEIGHT_SMALL / 2
    arranged_tiles = [[]]
    spawn_tile = None

    brains = list()
    fluffs = list()
    chests = list()
    relics = list()
    story = list()

    for i in content:
        if len(i) in (4, 5):
            tile = Tile(
                asset_handler,
                x, y,
                i[0],
                i[1],
                i[2],
                i[3]
            )

            if i[0] == 3:
                brains.append(Brain(tile, asset_handler))
            elif i[0] == 4:
                fluffs.append(Fluff(tile, asset_handler))
            elif i[0] == 5:
                chests.append(Chest(tile, asset_handler))
            elif i[0] == 6:
                relics.append(Relic(tile, asset_handler))

            tiles.append(tile)
            arranged_tiles[-1].append(tile)

            x += x_add

            if len(i) == 5:
                if i[-1] is True:
                    spawn_tile = tile
                else:
                    tile.story = i[-1]

        elif len(i) == 1:
            if i[0] == 0:
                y += y_add
                next_x.reverse()
                x = next_x[0]
                arranged_tiles.append(list())
            elif i[0] == 1:
                tiles.append(TileStopper())
                x += x_add

    arranged_tiles = arranged_tiles[:-1]

    #####
    # print(arranged_tiles)
    """Not all tile stoppers have to be unique."""
    tile_stopper = TileStopper()

    beginning = False
    for i in arranged_tiles:
        if beginning:
            i.insert(0, tile_stopper)
        else:
            i.append(tile_stopper)
        beginning = not beginning

    # print(arranged_tiles)

    """Add a list whith tile stoppers at index 0, with length of 1 + the length of the previous list at that index."""
    x = list()
    for i in range(0, len(arranged_tiles[0]) + 1, 1):
        x.append(tile_stopper)
    arranged_tiles.insert(0, x)
    # print(arranged_tiles)

    """Add a list whith tile stoppers at index -1, with length of 1 + the length of the previous list at that index."""
    x = list()
    for i in range(0, len(arranged_tiles[-1]) + 1, 1):
        x.append(tile_stopper)
    arranged_tiles.append(x)
    # print(arranged_tiles)
    



    ignore_first = True
    for _list in range(1 , len(arranged_tiles) - 1, 1):
        if ignore_first:
            for tile in range(0, len(arranged_tiles[_list]) - 1, 1):
                x = arranged_tiles[_list][tile]
                x.top_left = arranged_tiles[_list - 1][tile]
                x.top_right = arranged_tiles[_list - 1][tile + 1]
                x.bottom_left = arranged_tiles[_list + 1][tile]
                x.bottom_right = arranged_tiles[_list + 1][tile + 1]
        else:
            for tile in range(1, len(arranged_tiles[_list]), 1):
                # print(len(arranged_tiles[_list]))
                x = arranged_tiles[_list][tile]
                x.top_left = arranged_tiles[_list - 1][tile - 1]
                x.top_right = arranged_tiles[_list - 1][tile]
                x.bottom_left = arranged_tiles[_list + 1][tile - 1]
                x.bottom_right = arranged_tiles[_list + 1][tile]

        ignore_first = not ignore_first

    for tile in tiles:
        tile.create_surf()

    to_remove = list()
    for i in tiles:
        if i.is_stopper:
            to_remove.append(i)

    for i in to_remove:
        tiles.remove(i)

    return tiles, spawn_tile, brains, fluffs, chests, relics
    #####

    tile_stopper = TileStopper()

    # top left tile
    x = arranged_tiles[0][0]
    x.top_left = TileStopper()
    x.top_right = TileStopper()
    x.bottom_left = TileStopper()
    if (len(arranged_tiles > 1)) and (len(arranged_tiles[1] > 0)):
        x.bottom_right = arranged_tiles[1][0]
    else:
        x.bottom_right = TileStopper()

    # top right tile
    x = arranged_tiles[0][-1]
    if x is not arranged_tiles[0][0]:
        x.top_left = TileStopper()
        x.top_right = TileStopper()
        if (len(arranged_tiles > 1)) and (len(arranged_tiles[1] > 0)):
            l1 = len(arranged_tiles[0])
            l2 = len(arranged_tiles[1])

            if l1 == l2:
                x.bottom_left = arranged_tiles[1][-2]
                x.bottom_right = arranged_tiles[1][-1]
            elif l1 == l2 - 1:
                x.bottom_left = arranged_tiles[1][-1]
                x.bottom_right = TileStopper()
            elif l2 > l1:
                pos = arranged_tiles[0].index(x)
                x.bottom_left = arranged_tiles[1][pos - 1]
                x.bottom_right = arranged_tiles[1][pos]
            else:
                x.bottom_left = TileStopper()
                x.bottom_right = TileStopper()
        else:
            x.bottom_left = TileStopper()
            x.bottom_right = TileStopper()

        # bottom left tile
    
    return tiles
