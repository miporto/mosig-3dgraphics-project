#!/usr/bin/env python3
"""
OpenGL Cubemap Wrapper
"""
# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
from PIL import Image               # load images for textures

class Cubemap:
    """ Helper class to create and automatically destroy cubemaps """
    def __init__(self, file, wrap_mode=GL.GL_REPEAT, min_filter=GL.GL_LINEAR,
                 mag_filter=GL.GL_LINEAR_MIPMAP_LINEAR):
        self.glid = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, self.glid)
        try:
            self.__load(file)

            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap_mode)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap_mode)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, min_filter)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, mag_filter)
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
            #message = 'Loaded textures %s\t(%s, %s, %s, %s)'
            #print(message % (file, tex.shape, wrap_mode, min_filter, mag_filter))
        except FileNotFoundError:
            print("ERROR: unable to load texture file %s" % file)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, 0)

    def __load(self, files):
        # helper array stores texture format for every pixel size 1..4
        txt_format = [GL.GL_LUMINANCE, GL.GL_LUMINANCE_ALPHA, GL.GL_RGB, GL.GL_RGBA]
        i = 0
        for file in files:
            # imports image as a numpy array in exactly right format
            tex = np.array(Image.open(file))
            txt_format = txt_format[0 if len(tex.shape) == 2 else tex.shape[2] - 1]
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL.GL_RGBA, tex.shape[1],
                            tex.shape[0], 0, txt_format, GL.GL_UNSIGNED_BYTE, tex)
            i += 1
            message = 'Loaded texture %s\t(%s)'
            print(message % (file, tex.shape))

    def __del__(self):  # delete GL texture from GPU when object dies
        GL.glDeleteTextures(self.glid)
