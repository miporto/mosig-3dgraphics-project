#!/usr/bin/env python3
"""
Main program and scene setup
"""
# Python built-in modules
import sys

# External, non built-in modules
import glfw                         # lean window system wrapper for OpenGL

from keyframe import KeyFrameControlNode
from loaders import load_textured
from transform import vec, quaternion, quaternion_from_euler
from viewer import Viewer

def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()

    translate_keys = {0: vec(0, 0, 0), 2: vec(0, .2, 0), 4: vec(0.3, 0, 0)}
    rotate_keys = {0: quaternion(), 2: quaternion_from_euler(180, 0, 180),
                   4: quaternion_from_euler(180, 0, 180), 6: quaternion()}
    scale_keys = {0: 0.5, 2: 0.3, 4: 0.6}
    keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(*[mesh for file in sys.argv[1:] for mesh in load_textured(file)])
    viewer.add(keynode)

    #txt = TexturedPlane('resources/grass.png')
    #viewer.add(txt)
    # place instances of our basic objects
    if len(sys.argv) < 2:
        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
              ' format supported by pyassimp.' % (sys.argv[0],))

    #viewer.add(*[mesh for file in sys.argv[1:] for mesh in load_textured(file)])
    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
