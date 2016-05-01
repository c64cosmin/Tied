import pyglet
from pyglet.gl import *

#global size of all tiles
tile_size = 16

def set_tile_size(size):
    tile_size = size

#class that defines all tiles
class tile:
    def __init__(self):
        #all tiles have the same size
        self.size = tile_size

        #use pyglet to create a texture
        self.image = pyglet.image.Texture.create(self.size, self.size).get_image_data()

        #then get data from it
        self.data = list(self.image.get_data('RGBA', self.size*4))

        #flag that marks if the image has changed
        self.dirty = True

    #set a pixel color [r,g,b,a] at position x, y
    def set_pixel(self, x, y, color):
        #calculate the offset for the pixel that we want to change
        pos = (x + y * self.size) * 4
        #change accordingly
        for i in range(0,4):
            self.data[pos + i] = color[i]

        self.dirty = True

    #get a pixel color [r,g,b,a] at position x, y
    def get_pixel(self, x, y):
        #create the array for the pixel
        pixel = [0,0,0,0]
        #calculate the offset for the pixel that we want to sample
        pos = (x + y * self.size) * 4
        #fill the pixel array
        for i in range(0,4):
            pixel[i] = self.data[pos + i]

        return pixel

    #recreate the texture using pyglet
    def update(self):
        if not self.dirty:
            return
        #update the data
        self.image.set_data('RGBA', self.size*4, bytes(self.data))

        texture = self.image.get_texture()
        #use openGL calls for setting the sampling strategy
        glBindTexture(GL_TEXTURE_2D, texture.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        self.dirty = False

    def draw(self, x, y, size):
        self.update()
        self.image.blit(x = x, y = y, width = size, height = size)

