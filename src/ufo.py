from transform import translate, scale ,vec,quaternion, quaternion_from_euler
from loaders import load_textured
from node import Node
from keyframe import KeyFrameControlNode

class UFO(Node):
    """Textured bunny"""
    def __init__(self):
        super().__init__(transform=(translate(0.5, -0.7, -0.1) @ scale(0.007) ))
        self.add(*load_textured('res/ufo/Low_poly_UFO.obj'))

class UFOLoader():
	def __init__(self):
		
		ufo=UFO()
		translate_UFO = {0: vec(0, 0, 0),20: vec(0.8,1,-.85)}
		rotate_UFO = {0: quaternion_from_euler(0,0,0),4: quaternion_from_euler(0,0,10),10: quaternion_from_euler(0,65,0),20:quaternion_from_euler(0,180,0)}
		keynode = KeyFrameControlNode(translate_UFO,rotate_UFO,{0:1, 15:0.7})
		keynode.add(ufo)
		self.ufo = keynode

	def get_ufo(self):
		return self.ufo
