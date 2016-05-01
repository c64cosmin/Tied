from pyglet.gl import *
import pyglet
import setup
from random import randint
app_window = pyglet.window.Window(resizable = True)
setup.setup(app_window)

if __name__ == '__main__':
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBlendEquation(GL_FUNC_ADD)

    app_window.set_size(800,600)
    app_window.set_minimum_size(800,600)

    pyglet.app.run()
