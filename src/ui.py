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

    def add_child(self, child):
        self.child.append(child)

    def propagate_event(self, event):
        for child in self.child:
            event = child.propagate_event(event)

        #handle the event and update the event state
        event = self.handle_event(self, event)

        #return the event for propagation
        return event

    def set_handle_event(self, func):
        self.handle_event = func

    def is_inside(self, event):
        x = event["x"]
        y = event["y"]
        if x < self.x or x > self.x + self.sx or y < self.y or y > self.y + self.sy:
            return False
        return True
