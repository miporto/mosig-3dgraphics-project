#!/usr/bin/env python3
"""
Skybox using cubemap
"""
# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np

from cubemap import Cubemap
from shader import Shader
from vertex_array import VertexArray

VEC_SHAD = """#version 330 core
layout (location = 0) in vec3 position;
out vec3 fragTexCoord;
uniform mat4 modelviewprojection;

void main() {
    fragTexCoord = position;
    gl_Position = modelviewprojection * vec4(position, 1.0);
}
"""

FRAG_SHAD = """#version 330 core
out vec4 FragColor;

in vec3 fragTexCoord;

uniform samplerCube skybox;

void main() {
    FragColor = texture(skybox, fragTexCoord);
}
"""

DEF_VERTICES = np.array((
    (-1.0, 1.0, -1.0),
    (-1.0, -1.0, -1.0),
    (1.0, -1.0, -1.0),
    (1.0, -1.0, -1.0),
    (1.0, 1.0, -1.0),
    (-1.0, 1.0, -1.0),

    (-1.0, -1.0,  1.0),
    (-1.0, -1.0, -1.0),
    (-1.0,  1.0, -1.0),
    (-1.0,  1.0, -1.0),
    (-1.0,  1.0,  1.0),
    (-1.0, -1.0,  1.0),

    (1.0, -1.0, -1.0),
    (1.0, -1.0,  1.0),
    (1.0,  1.0,  1.0),
    (1.0,  1.0,  1.0),
    (1.0,  1.0, -1.0),
    (1.0, -1.0, -1.0),

    (-1.0, -1.0,  1.0),
    (-1.0,  1.0,  1.0),
    (1.0,  1.0,  1.0),
    (1.0,  1.0,  1.0),
    (1.0, -1.0,  1.0),
    (-1.0, -1.0,  1.0),

    (-1.0,  1.0, -1.0),
    (1.0,  1.0, -1.0),
    (1.0,  1.0,  1.0),
    (1.0,  1.0,  1.0),
    (-1.0,  1.0,  1.0),
    (-1.0,  1.0, -1.0),

    (-1.0, -1.0, -1.0),
    (-1.0, -1.0,  1.0),
    (1.0, -1.0, -1.0),
    (1.0, -1.0, -1.0),
    (-1.0, -1.0,  1.0),
    (1.0, -1.0,  1.0)), 'f')

class Skybox:
    def __init__(self, files, attributes=[DEF_VERTICES]):
        self.shader = Shader(VEC_SHAD, FRAG_SHAD)
        self.vertex_array = VertexArray(attributes)
        self.cubemap = Cubemap(files)

    def draw(self, projection, view, model, color_shader=None, win=None, **param):
        """ Draw object """
        GL.glDepthFunc(GL.GL_LEQUAL)
        #GL.glDepthMask(GL.GL_FALSE)

        GL.glUseProgram(self.shader.glid)

        # projection geometry
        loc = GL.glGetUniformLocation(self.shader.glid, 'modelviewprojection')
        # it seems not to be working as expected 
        # I want to remove the translation from the view matrix
        np.resize(view, (3, 3))
        np.resize(view, (4, 4))
        GL.glUniformMatrix4fv(loc, 1, True, projection @ view @ np.identity(4, 'f'))

        # texture access setups
        loc = GL.glGetUniformLocation(self.shader.glid, 'skybox')
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, self.cubemap.glid)
        GL.glUniform1i(loc, 0)
        self.vertex_array.execute(GL.GL_TRIANGLES)

        #GL.glDepthMask(GL.GL_TRUE)
        GL.glDepthFunc(GL.GL_LESS)
        # leave clean state for easier debugging
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, 0)
        GL.glUseProgram(0)

