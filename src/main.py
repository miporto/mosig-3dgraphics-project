#!/usr/bin/env python3
"""
Main program and scene setup
"""
# Python built-in modules
import sys

# External, non built-in modules
import glfw                         # lean window system wrapper for OpenGL

from keyframe import KeyFrameControlNode
from loaders import load, load_textured
from skybox import Skybox
from transform import vec, quaternion, quaternion_from_euler,scale, translate
from viewer import Viewer
from spaceship import Spaceship
from node import *
from planet import *
from asteroidLoader import *

def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()

    # place instances of our basic objects
    if len(sys.argv) < 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by pyassimp.' % (sys.argv[0],))

    viewer.add(movingAsteroids().get_cluster())
    viewer.add_movable(Spaceship())
    
    sea = [
        'res/skybox/right.jpg',
        'res/skybox/left.jpg',
        'res/skybox/top.jpg',
        'res/skybox/bottom.jpg',
        'res/skybox/front.jpg',
        'res/skybox/back.jpg'
    ]
    moonwaw = [
        'res/mp_moonwaw/moonwaw_lf.tga',
        'res/mp_moonwaw/moonwaw_rt.tga',
        'res/mp_moonwaw/moonwaw_up.tga',
        'res/mp_moonwaw/moonwaw_dn.tga',
        'res/mp_moonwaw/moonwaw_ft.tga',
        'res/mp_moonwaw/moonwaw_bk.tga']
    blood_valley = [
        'res/mp_bloodvalley/blood-valley_lf.tga',
        'res/mp_bloodvalley/blood-valley_rt.tga',
        'res/mp_bloodvalley/blood-valley_up.tga',
        'res/mp_bloodvalley/blood-valley_dn.tga',
        'res/mp_bloodvalley/blood-valley_ft.tga',
        'res/mp_bloodvalley/blood-valley_bk.tga']
    viewer.add(Skybox(blood_valley))
   
    viewer.add(PlanetLoader().get_planet())
    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
