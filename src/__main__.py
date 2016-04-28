import pyglet
import gfx
from ctypes import *
from pyglet.gl import *
from random import randint
app_window = pyglet.window.Window(resizable = True)
app_window.image = gfx.tile()
@app_window.event
def on_draw():
    glClearColor(0, 0, 0, 255)
    app_window.clear()
    for x in range(0,app_window.image.size):
        for y in range(0,app_window.image.size):
            app_window.image.set_pixel(x, y, [x*15, y*15, 0, x*15])
    app_window.image.update()
    app_window.image.draw(10,10, randint(9,10))
if __name__ == '__main__':
    def foo(value):
        print (str(value))
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glBlendEquation(GL_FUNC_ADD); 
    pyglet.clock.schedule_interval(foo, 1.0/3.0)
    app_window.set_size(800,600)
    app_window.set_minimum_size(800,600)
    pyglet.app.run()
