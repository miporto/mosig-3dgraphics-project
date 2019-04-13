#!/usr/bin/env python3
"""
Mesh classes
"""
# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper

from shader import Shader
from texture import Texture
from vertex_array import VertexArray

# -------------- Example texture plane class ----------------------------------
TEXTURE_VERT = """#version 330 core
uniform mat4 modelviewprojection;
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 tex_coords;
out vec2 fragTexCoord;
void main() {
    gl_Position = modelviewprojection * vec4(position, 1);
    fragTexCoord = tex_coords;
}"""

TEXTURE_FRAG = """#version 330 core
uniform sampler2D diffuseMap;
in vec2 fragTexCoord;

out vec4 outColor;

void main() {
    outColor = texture(diffuseMap, fragTexCoord);
}"""

class ColorMesh:
    """ Color Mesh class """

    def __init__(self, attributes, index=None):
        self.vertex_array = VertexArray(attributes, index)

    def draw(self, projection, view, model, color_shader, **param):
        """ Draw object """

        names = ['view', 'projection', 'model']
        loc = {n: GL.glGetUniformLocation(color_shader.glid, n) for n in names}
        GL.glUseProgram(color_shader.glid)

        GL.glUniformMatrix4fv(loc['view'], 1, True, view)
        GL.glUniformMatrix4fv(loc['projection'], 1, True, projection)
        GL.glUniformMatrix4fv(loc['model'], 1, True, model)

        # draw triangle as GL_TRIANGLE vertex array, draw array call
        self.vertex_array.execute(GL.GL_TRIANGLES)

class TexturedMesh:
    """ Color Mesh class """

    def __init__(self, file, attributes, index=None,frag_shader=TEXTURE_FRAG):
        self.shader = Shader(TEXTURE_VERT, frag_shader)
        self.texture = Texture(file)
        self.vertex_array = VertexArray(attributes, index)

    def draw(self, projection, view, model, color_shader=None, win=None, **param):
        """ Draw object """

        GL.glUseProgram(self.shader.glid)

        # projection geometry
        loc = GL.glGetUniformLocation(self.shader.glid, 'modelviewprojection')
        GL.glUniformMatrix4fv(loc, 1, True, projection @ view @ model)

        # texture access setups
        loc = GL.glGetUniformLocation(self.shader.glid, 'diffuseMap')
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.glid)
        GL.glUniform1i(loc, 0)
        self.vertex_array.execute(GL.GL_TRIANGLES)

        # leave clean state for easier debugging
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glUseProgram(0)
