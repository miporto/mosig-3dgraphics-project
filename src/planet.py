from transform import translate, scale,vec ,quaternion_from_euler
from loaders import load_textured
from node import *
from keyframe import KeyFrameControlNode

class Planet(Node):
    """Keyboard movable spaceship"""
    def __init__(self):
    	super().__init__(transform = scale(0.03,0.03,0.03) )
    	self.add(*load_textured('res/satellite/Mars 2K.obj'))    

class PlanetLoader():
	def __init__(self):

		planet = Planet()

		rotate_planet = {0: quaternion_from_euler(0,0,0), 2: quaternion_from_euler(0,15,0),20:quaternion_from_euler(0,90,0)}
		keynode = KeyFrameControlNode({0:vec(.8,.8,-.9)},rotate_planet,{0:1, 2:1})
		keynode.add(planet)
		self.satellite = keynode

	def get_planet(self):
		return self.satellite
