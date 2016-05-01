class area:
    #create a new ui area at position (x,y) with size (sx,sy)
    def __init__(self, x, y, sx, sy):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        
        #list with all the contained childs
        self.child = []

        #handle_event must be set after the creation of the object
        @self.set_handle_event
        def handle_event(self, event):
            return event

        @self.set_draw
        def draw(self):
            pass

    def add_child(self, child):
        self.child.append(child)

    def propagate_event(self, event):
        for child in self.child:
            event = self.propagate_event(event)

        #handle the event and update the event state
        event = self.handle_event(self, event)

        #return the event for propagation
        return event

    def set_handle_event(self, func):
        self.handle_event = func

    def set_draw(self, func):
        self.draw = func
