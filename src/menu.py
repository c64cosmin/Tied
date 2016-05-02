import pyglet
import gfx
import map
import ui
from pyglet.gl import *
from random import randint
from math import floor
from math import cos
from math import sin
from math import pi
import colorsys

#this class defines all the right side tile bar
#including the addition of new tiles, cloning them
#and changing the palettes for palette tiles
class tile_bar:
    #selection of the tile
    select = -1;
    #hold instance for static access
    instance = None

    def __init__(self):
        tile_bar.instance = self
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
                #is the event inside the area
                if event_self.is_inside(event):
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

                self.button_area.x = event["x"] - self.area.sx

                #let the event be treated by other areas
                return event

            #handle scroll event
            if event["type"] == "scroll":
                if event_self.is_inside(event):
                    self.scroll -= event["sy"]
                    if self.scroll > len(self.tiles) * 128 - self.area.sy + 32:
                        self.scroll = len(self.tiles) * 128 - self.area.sy + 32
                    if self.scroll < 0:
                        self.scroll = 0

                    #consume the event
                    return None

            #see what tile was selected
            if event["type"] == "release":
                #see if the click was made inside the area
                if event_self.is_inside(event):
                    #is the button pressed the left one
                    if event["button"] == 1:
                        y = event["y"]
                        tile_bar.select = int((self.area.sy - y + self.scroll)/128)
                        if(tile_bar.select < 0):
                            tile_bar.select = 0
                        if(tile_bar.select >= len(self.tiles)):
                            tile_bar.select = len(self.tiles)-1

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

    def get_selection():
        if tile_bar.select == -1:
            return None

        return tile_bar.instance.tiles[tile_bar.select]

    def draw(self):
        for i in range(len(self.tiles)):
            self.tiles[i].draw(self.area.x, self.area.sy + self.scroll - (i+1)*128, 128)
        self.selection.blit(self.area.x, self.area.sy + self.scroll - (tile_bar.select+1)*128)
        self.button.blit(self.area.x, 0)



#this class defines the drawing area of the editor
class draw_area:
    def __init__(self):
        self.map = map.test_map()
        #scroll for the test map
        self.scroll_x = 0
        self.scroll_y = 0
        #does the test map have at least one tile
        self.initiated = False
        #pixel size for the map
        self.zoom = 4

        self.area = ui.area(0,0, 800,600)

        @self.area.set_handle_event
        def handle_event(event_self, event):
            if event is None:
                return event

            #see if the area was clicked
            if event["type"] == "release" or event["type"] == "drag":
                #map coordinates
                pos_x = floor((event["x"] - self.scroll_x)/(self.zoom * gfx.tile_size))
                pos_y = floor((event["y"] - self.scroll_y)/(self.zoom * gfx.tile_size))
                #it's always inside
                #see if the button is the left one
                if event["button"] == 1:
                    if not self.initiated and tile_bar.get_selection() is not None:
                        self.initiated = True
                        self.scroll_x = event["x"]
                        self.scroll_y = event["y"]
                        pos_x = 0
                        pos_y = 0
                    self.map.add_tile(pos_x, pos_y, tile_bar.get_selection())
                    return None

                if event["button"] == 4:
                    self.map.delete_tile(pos_x, pos_y)
                    return None

            #drag the test map
            if event["type"] == "drag":
                if event["button"] == 2:
                    self.scroll_x += event["dx"]
                    self.scroll_y += event["dy"]

                    return None

            #zoom in zoom out
            if event["type"] == "scroll":
                old_zoom = self.zoom
                self.zoom += event["sy"]

                if(self.zoom < 1):
                    self.zoom = 1

                #must change scroll position with respect to the mouse position
                dx = (self.scroll_x - event["x"]) / old_zoom
                dy = (self.scroll_y - event["y"]) / old_zoom
                #solve for scroll position
                self.scroll_x = dx * self.zoom + event["x"]
                self.scroll_y = dy * self.zoom + event["y"]

                return None

            #did we resize
            if event["type"] == "resize":
                self.area.sx = event["x"]
                self.area.sy = event["y"]
                return event

            #propagate the rest of the events
            return event


    def draw(self):
        self.map.draw(self.scroll_x, self.scroll_y, self.zoom)
        if tile_bar.get_selection() is not None:
            tile_bar.get_selection().draw(self.scroll_x, self.scroll_y, 10)



#this class defines a color picker
class color_picker:
    def __init__(self):
        #the clickable area for the color picker
        self.area = ui.area(0,0, 200, 200)

        #outer&inner radiuses for the color wheel
        self.max_rad = 0.5
        self.min_rad = 0.4
        #the color picker vertex buffer
        self.color_wheel = self.make_color_wheel()
        #the hue angle
        self.hue_angle = 0
        #indicator circle for the hue angle
        self.circle = pyglet.image.load("img/circle16.png")

        #saturation and value indicator values
        self.saturation = 0
        self.value = 0

        self.color = [0,0,0]


    #creates a color wheel
    def make_color_wheel(self):
        vertices = []
        colors = []
        for angle in range(0, 370, 10):
            x = cos(angle*pi/180)*self.area.sx*self.max_rad + self.area.sx/2
            y = sin(angle*pi/180)*self.area.sx*self.max_rad + self.area.sx/2
            vertices.append(x)
            vertices.append(y)
            x = cos(angle*pi/180)*self.area.sx*self.min_rad + self.area.sx/2
            y = sin(angle*pi/180)*self.area.sx*self.min_rad + self.area.sx/2
            vertices.append(x)
            vertices.append(y)
            color = colorsys.hsv_to_rgb(angle/360, 1.0, 1.0)
            for t in range(2):
                for i in range(3):
                    colors.append(int(color[i]*255))
        color_wheel = pyglet.graphics.vertex_list(int(len(vertices)/2), ('v2f', vertices), ('c3B', colors))
        return color_wheel


    #draws the hue angle indicator
    def draw_hue_angle(self):
        x = cos(self.hue_angle*pi/180)*self.area.sx*(self.max_rad+self.min_rad)/2 + self.area.sx/2
        y = sin(self.hue_angle*pi/180)*self.area.sx*(self.max_rad+self.min_rad)/2 + self.area.sx/2

        x = int(x)
        y = int(y)

        self.circle.blit(x-8, y-8)


    #draw the picking square
    def draw_pick_square(self):
        vertices = []
        colors = []

        x = cos(pi*3/4)*self.area.sx*self.min_rad + self.area.sx/2

        s = (cos(pi/4)-cos(pi*3/4))*self.area.sx*self.min_rad

        vert = [[0,0], [0,1], [1,0], [1,1]]

        for x_pos in range(10):
            for y_pos in range(10):
                for point in vert:
                    xp = (x_pos+point[0])/10
                    yp = (y_pos+point[1])/10
                    vertices.append(x + s*xp)
                    vertices.append(x + s*yp)

                    color = colorsys.hsv_to_rgb(self.hue_angle/360, xp, yp)
                    for i in range(3):
                        colors.append(int(color[i]*255))

        pyglet.graphics.draw(int(len(vertices)/2), pyglet.gl.GL_TRIANGLE_STRIP, ('v2f', vertices), ('c3B', colors))

        #draw the picking square indicator
        vertices = []
        colors = []

        lines = [1, -1]
        for add in lines:
            #horizontal
            vertices.append(x)
            vertices.append(x + s*self.value + add)

            vertices.append(x+s)
            vertices.append(x + s*self.value + add)

            #vertical
            vertices.append(x + s*self.saturation + add)
            vertices.append(x)

            vertices.append(x + s*self.saturation + add)
            vertices.append(x+s)

        #for each vertex add one black color (i.e three zeros)
        for t in range(int(len(vertices)/2) * 3):
            colors.append(0)

        #horizontal
        vertices.append(x)
        vertices.append(x + s*self.value)

        vertices.append(x+s)
        vertices.append(x + s*self.value)

        #vertical
        vertices.append(x + s*self.saturation)
        vertices.append(x)

        vertices.append(x + s*self.saturation)
        vertices.append(x+s)

        #for the rest of 4 vertices add the color white
        for t in range(4):
            for i in range(3):
                colors.append(255)

        pyglet.graphics.draw(int(len(vertices)/2), pyglet.gl.GL_LINES, ('v2f', vertices), ('c3B', colors))


    #draw the color preview
    def draw_color_preview(self):
        vertices = []
        colors = []

        vert = [[0,0], [1,0], [0,1], [1,0], [0,1], [1,1]]

        def add_square(x, y, sx, sy, color):
            for point in vert:
                vertices.append(x + sx*point[0])
                vertices.append(y + sy*point[1])

                colors.append(color[0])
                colors.append(color[1])
                colors.append(color[2])

        color = self.get_color();

        #black background square
        add_square(0, self.area.sx, self.area.sx/2, 40, [0,0,0])
        #white background square
        add_square(self.area.sx/2, self.area.sx, self.area.sx/2, 40, [255,255,255])

        #preview
        add_square(10, self.area.sx+10, self.area.sx/2-20, 40-20, color)
        add_square(self.area.sx/2+10, self.area.sx+10, self.area.sx/2-20, 40-20, color)

        #big preview
        add_square(0, self.area.sx+40, self.area.sx, 40, color)

        pyglet.graphics.draw(int(len(vertices)/2), pyglet.gl.GL_TRIANGLES, ('v2f', vertices), ('c3B', colors))


    def update_color(self):
        color = colorsys.hsv_to_rgb(self.hue_angle/360, self.saturation, self.value)
        for i in range(3):
            self.color[i] = int(color[i]*255)


    def set_color(self, color):
        new_values = colorsys.rgb_to_hsv(color[0]/255, color[1]/255, color[2]/255)
        self.hue_angle = new_values[0]*360
        self.saturation = new_values[1]
        self.value = new_values[2]
        self.color = color


    def get_color(self):
        self.update_color()
        return self.color


    def draw(self):
        self.color_wheel.draw(pyglet.gl.GL_TRIANGLE_STRIP)

        self.draw_hue_angle()
        self.draw_pick_square()
        self.draw_color_preview()
