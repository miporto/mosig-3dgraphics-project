from node import Node
from transform import translate, scale
from loaders import load_textured

class Spaceship(Node):
    """Keyboard movable spaceship"""
    def __init__(self):
        super().__init__(transform=(scale(0.5) @ translate(0.75, 0, -1)))
        self.add(*load_textured('res/textured_ship/Sample_Ship.obj'))
