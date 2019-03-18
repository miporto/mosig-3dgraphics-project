#!/usr/bin/env python3
"""
Skybox using cubemap
"""
# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper

from cubemap import Cubemap
from shader import Shader
from vertex_array import VertexArray

VEC_SHAD = """#version 330 core
layout (location = 0) in vec3 aPos;

out vec3 TexCoords;

uniform mat4 modelviewprojection;

void main() {
    TexCoords = aPos;
    gl_Position = modelviewprojection * vec4(aPos, 1.0);
}
"""

FRAG_SHAD = """#version 330 core
out vec4 FragColor;

in vec3 TexCoords;

uniform samplerCube skybox;

void main() {
    FragColor = texture(skybox, TexCoords);
}
"""

class Skybox:
    def __init__(self, files, attributes):
        self.shader = Shader(VEC_SHAD, FRAG_SHAD)
        self.cubemap = Cubemap(files)
        self.vertex_array = VertexArray(attributes)

    def draw(self, projection, view, model, color_shader=None, win=None, **param):
        """ Draw object """
        GL.glDepthFunc(GL.GL_LEQUAL)

        GL.glUseProgram(self.shader.glid)

        # projection geometry
        loc = GL.glGetUniformLocation(self.shader.glid, 'modelviewprojection')
        GL.glUniformMatrix4fv(loc, 1, True, projection @ view @ model)

        # texture access setups
        loc = GL.glGetUniformLocation(self.shader.glid, 'diffuseMap')
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, self.cubemap.glid)
        GL.glUniform1i(loc, 0)
        self.vertex_array.execute(GL.GL_TRIANGLES)

        GL.glDepthFunc(GL.GL_LESS)
        # leave clean state for easier debugging
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, 0)
        GL.glUseProgram(0)

