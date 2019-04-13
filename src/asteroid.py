from node import Node
from transform import translate, scale
from loaders import load_textured

class Asteroid(Node):
    """Asteroid"""
    def __init__(self):
        super().__init__(transform=(scale(0.006)))
        self.add(*load_textured('res/asteroid/asteroid.obj'))
 	