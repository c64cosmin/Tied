import gfx

class test_map:
    def __init__(self):
        #list that holds the tiles
        #it's not a matrix, because it should not have a width/height limit
        #the map's purpose is just for testing
        self.tiles = []

    def add_tile(self, x, y, tile):
        #see if we got a valid tile
        if tile is None:
            return
        #find if we can add the tile
        for t in self.tiles:
            if t[1] == x and t[2] == y:
                #there is a tile on that position
                return

        self.tiles.append([tile, x, y])

    def delete_tile(self, x, y):
        #find the tile at position x,y
        for tile in self.tiles:
            if tile[1] == x and tile[2] == y:
                self.tiles.remove(tile)
                return

    def draw(self, x, y, pixel_size):
        for tile in self.tiles:
            #draw everytile offset to it's position
            tile[0].draw(x + tile[1] * pixel_size * gfx.tile_size,
                         y + tile[2] * pixel_size * gfx.tile_size,
                         pixel_size * gfx.tile_size) 
