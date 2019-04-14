#!/usr/bin/env python3
"""
Main program and scene setup
"""
# Python built-in modules

# External, non built-in modules
import glfw                         # lean window system wrapper for OpenGL

from skybox import Skybox
from viewer import Viewer
from spaceship import Spaceship
from planet import PlanetLoader
from asteroidLoader import MovingAsteroids
from ufo import UFO



def main():
    """ create a window, add scene objects, then run rendering loop """

    viewer = Viewer(1900,1200)
    viewer.add(MovingAsteroids().get_cluster())
    viewer.add_movable(Spaceship())
    viewer.add(PlanetLoader().get_planet())
    viewer.add(UFO())
    
    blood_valley = [
        'res/mp_bloodvalley/blood-valley_lf.tga',
        'res/mp_bloodvalley/blood-valley_rt.tga',
        'res/mp_bloodvalley/blood-valley_up.tga',
        'res/mp_bloodvalley/blood-valley_dn.tga',
        'res/mp_bloodvalley/blood-valley_ft.tga',
        'res/mp_bloodvalley/blood-valley_bk.tga']
    viewer.add(Skybox(blood_valley))

    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
