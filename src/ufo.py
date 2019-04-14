from transform import translate, scale
from loaders import load_textured
from node import Node

class UFO(Node):
    """Textured bunny"""
    def __init__(self):
        super().__init__(transform=(scale(0.009) @ translate(0.92, -0.32, -1)))
        self.add(*load_textured('res/ufo/Low_poly_UFO.obj'))
