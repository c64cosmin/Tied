import pyglet
import gfx
import ui
from random import randint

class tile_bar:
    def __init__(self):
        #list of all available tiles
        self.tiles = []

        #tile selection image
        self.selection = pyglet.image.load("img/selection.png")
        #add new tile image
        self.button = pyglet.image.load("img/addtile.png")
        #an area for the button
        self.button_area = ui.area(800-128, 0, 128, 32)
        @self.button_area.set_handle_event
        def handle_event(event_self, event):
            if event is None:
                return event

            #is the button clicked
            if event["type"] == "release":
                #is the button released the left one
                if event["button"] == 1:
                    self.add_new_tile()
                    #consume the event
                    return None

            #return other event to be treated by other areas
            return event

        #value that stores the scroll of the tiles
        self.scroll = 0

        #an area that defines the tiles bar
        self.area = ui.area(800-128, 0, 128, 600)
        #add the button area as a child to the tile bar
        self.area.add_child(self.button_area)

        @self.area.set_handle_event
        def handle_event(event_self, event):
            if event is None:
                return event
            
            #always put the tile bar on the right of the window
            if event["type"] == "resize":
                self.area.x = event["x"] - self.area.sx
                self.area.sy = event["y"]

                #let the event be treated by other areas
                return event
                
            if event["type"] == "scroll":
                print(event_self.is_inside(event))
                if event_self.is_inside(event):
                    self.scroll -= event["sy"]
                    if self.scroll > len(self.tiles) * 128 - self.area.sy + 32:
                        self.scroll = len(self.tiles) * 128 - self.area.sy + 32
                    if self.scroll < 0:
                        self.scroll = 0

                    #consume the event
                    return None

            #return other event to be treated by other areas
            return event

    def add_new_tile(self):
        #create a new tile
        tile = gfx.tile()

        #choose a random color
        color = [randint(0,255), randint(0,255), randint(0,255), 255]

        for x in range(tile.size):
            for y in range(tile.size):
                tile.set_pixel(x, y, color)

        #add the new tile to the rest
        self.tiles.append(tile)

    def draw(self, selection = -1):
        for i in range(len(self.tiles)):
            self.tiles[i].draw(self.area.x, self.area.sy + self.scroll - (i+1)*128, 128)
        self.selection.blit(self.area.x, self.area.sy + self.scroll - selection*128)
        self.button.blit(self.area.x, 0)
