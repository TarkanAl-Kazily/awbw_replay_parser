

import enum

class Tiles(enum.IntEnum):
    ROAD = 0
    PLAIN = 1
    FOREST = 2
    CITY = 3
    PIPE = 4

class Map():

    def __init__(self):
        """
        An Advance Wars map class
        """
        self._w = 10
        self._h = 10
        self._map = [Tiles.ROAD for x in range(self._w * self._h)]

    def render(self):
        """
        TODO: Uses the arcade library and the library of tiles to draw on the screen
        """
        pass

    def get(x, y):
        return self._map[x + self._w * y]

    def set(x, y, tile):
        self._map[x + self._w * y] = tile
