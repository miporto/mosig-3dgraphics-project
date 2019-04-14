from node import Node
from loaders import load_textured
from asteroid import Asteroid
from transform import Trackball, identity, translate, rotate, scale ,vec,quaternion, quaternion_from_euler
from keyframe import KeyFrameControlNode
class AsteroidGroup():
    """Asteroid"""
    def __init__(self):

        asteroid = Asteroid()

        first_asteroid = Node(transform=(scale(2,2,2)))
        first_asteroid.add(asteroid)

        second_asteroid = Node(transform=(translate(0.4, 0.2, 0.5) @ scale(1, 1, 1)))
        second_asteroid.add(asteroid)
        third_asteroid = Node(transform=(translate(0.3, 0.3, 0.5) @ scale(0.75, 1, 0.75)))
        third_asteroid.add(asteroid)
        fourth_asteroid = Node(transform=(translate(0.35,0.25, 0.35) @ scale(1.5, 1.25, 1.5)))
        fourth_asteroid.add(asteroid)
        fifth_asteroid = Node(transform=(translate(0.5, 0.35, 0.4) @ scale(0.5, 0.5, 0.7)))
        fifth_asteroid.add(asteroid)

        theta = 70      
        phi1 = 30
        phi2 = 110
        phi3 = 20
        phi4 = 45

        transform_fifth_asteroid = Node(transform=rotate((3, 2, 0), phi4))
        transform_fifth_asteroid.add(fifth_asteroid)

        transform_fourth_asteroid = Node(transform=rotate((1, 4, 2), phi1))
        transform_fourth_asteroid.add(fourth_asteroid,transform_fifth_asteroid)

        transform_third_asteroid = Node(transform=rotate((1, 0, 3), phi2))
        transform_third_asteroid.add(third_asteroid,transform_fourth_asteroid)

        transform_second_asteroid = Node(transform=rotate((4, 2, 1), phi3))
        transform_second_asteroid.add(second_asteroid, transform_third_asteroid)

        transform_first_asteroid = Node(transform=rotate((3, 3, 0), theta))
        transform_first_asteroid.add(first_asteroid, transform_second_asteroid)

        self.cloud = transform_first_asteroid

    def get_cloud(self):
        return self.cloud
			
			

class MovingAsteroids():
	def __init__(self):

		group = AsteroidGroup()
		translate_keys = {0: vec(1, 0.6, 0),20: vec(-2,0.6,0)}
		rotate_keys = {0: quaternion_from_euler(),5: quaternion_from_euler(45, 0, 45),10: quaternion_from_euler(90, 0, 90),15: quaternion_from_euler(135, 0, 135),20: quaternion_from_euler(180, 0, 180)}
		scale_keys = {0: 1}
		keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
		keynode.add(group.get_cloud())
		self.asteroid_cluster=keynode

	def get_cluster(self):
		return self.asteroid_cluster
