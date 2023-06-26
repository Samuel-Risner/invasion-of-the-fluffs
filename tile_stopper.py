class TileStopper():

    def __init__(self):
        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None

        self.is_stopper = True
        self.visible = False
        self.tile_contents = -1
        self.traversable = False

    def create_surf(self):
        pass

    def draw(self, _):
        pass

    def show(self, _):
        pass