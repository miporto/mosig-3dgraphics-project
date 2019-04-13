from node import Node
from transform import translate, scale
from loaders import load_textured
from asteroid import Asteroid
from transform import Trackball, identity, translate, rotate, scale

class AsteroidLoader():
    """Asteroid"""
    def __init__(self):
        super().__init__()

        asteroid = Asteroid()

        first_asteroid = Node(transform=(scale(3,3,3)))
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
			