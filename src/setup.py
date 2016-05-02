import pyglet
from pyglet.gl import *
import ui
import menu
from random import randint
def setup(window):
    window.window_area = ui.area(0, 0, 800, 600)
    @window.window_area.set_handle_event
    def handle_event(self, event):
        if event is None:
            return event
        return event

    #add a color picker
    window.color_picker = menu.color_picker()
    window.window_area.add_child(window.color_picker.area)

    #add the drawing area to the window
    window.draw_area = menu.draw_area()
    window.window_area.add_child(window.draw_area.area)

    #add the tile bar to the window
    window.tile_bar = menu.tile_bar()
    window.draw_area.area.add_child(window.tile_bar.area)


    @window.event
    def on_draw():
        glClearColor(0, 0, 0, 255)
        window.clear()
        window.draw_area.draw()
        window.tile_bar.draw()
        window.color_picker.draw()


    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            return pyglet.event.EVENT_HANDLED


    @window.event
    def on_resize(width, height):
        event = {}
        event["x"] = width
        event["y"] = height
        event["type"] = "resize"

        window.window_area.propagate_event(event)


    @window.event
    def on_mouse_motion(x, y, dx, dy):
        event = {}
        event["x"] = x
        event["y"] = y
        event["type"] = "move"

        window.window_area.propagate_event(event)


    @window.event
    def on_mouse_press(x, y, button, modifiers):
        event = {}
        event["x"] = x
        event["y"] = y
        event["type"] = "press"
        event["button"] = button

        window.window_area.propagate_event(event)


    @window.event
    def on_mouse_release(x, y, button, modifiers):
        event = {}
        event["x"] = x
        event["y"] = y
        event["type"] = "release"
        event["button"] = button

        window.window_area.propagate_event(event)


    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        event = {}
        event["x"] = x
        event["y"] = y
        event["dx"] = dx
        event["dy"] = dy
        event["type"] = "drag"
        event["button"] = buttons

        window.window_area.propagate_event(event)


    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        event = {}
        event["x"] = x
        event["y"] = y
        event["sx"] = scroll_x
        event["sy"] = scroll_y
        event["type"] = "scroll"

        window.window_area.propagate_event(event)
