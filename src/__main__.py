import pyglet
import gfx
import map
import ui
import sys
from ctypes import *
from pyglet.gl import *
from random import randint
app_window = pyglet.window.Window(resizable = True)


@app_window.event
def on_draw():
    glClearColor(0, 0, 0, 255)
    app_window.clear()


@app_window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        return pyglet.event.EVENT_HANDLED


@app_window.event
def on_resize(width, height):
    app_window.window_area.sx = width
    app_window.window_area.sy = height


@app_window.event
def on_mouse_motion(x, y, dx, dy):
    event = {}
    event["x"] = x
    event["y"] = y
    event["type"] = "move"

    app_window.window_area.propagate_event(event)


@app_window.event
def on_mouse_press(x, y, button, modifiers):
    event = {}
    event["x"] = x
    event["y"] = y
    event["type"] = "press"
    event["button"] = button

    app_window.window_area.propagate_event(event)


@app_window.event
def on_mouse_release(x, y, button, modifiers)
    event = {}
    event["x"] = x
    event["y"] = y
    event["type"] = "release"
    event["button"] = button

    app_window.window_area.propagate_event(event)


@app_window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers)
    event = {}
    event["x"] = x
    event["y"] = y
    event["type"] = "drag"
    event["button"] = buttons

    app_window.window_area.propagate_event(event)


if __name__ == '__main__':
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBlendEquation(GL_FUNC_ADD)

    app_window.set_size(800,600)
    app_window.set_minimum_size(800,600)

    app_window.window_area = ui.area(0, 0, 800, 600)

    def handle_event(self, event):
        print(self.x)
        print(self.y)
        print(self.sx)
        print(self.sy)
        print(event["x"])
        print(event["y"])
        print(event["type"])
        sys.stdout.flush()
    app_window.window_area.handle_event = handle_event
    pyglet.app.run()
