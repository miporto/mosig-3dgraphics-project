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
TEXTURE_VERT_2 = """#version 330 core
uniform mat4 modelviewprojection;
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 tex_coords;
out vec2 fragTexCoord;
void main() {
    gl_Position = modelviewprojection * vec4(position, 1);
    fragTexCoord = tex_coords;
}"""

TEXTURE_VERT = """#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 tex_coords;
layout(location = 2) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
out vec3 fragNormal;
out vec3 fragView;
out vec2 fragTexCoord;
void main() {
    gl_Position = projection * view * model * vec4(position, 1);
    fragNormal = normal; // fixed light
    // fragNormal = transpose(inverse(mat3(view * model))) * normal;
    fragView = normalize((view * model * vec4(position, 1)).xyz);
    fragTexCoord = tex_coords;
}"""

TEXTURE_FRAG_2 = """#version 330 core
uniform sampler2D diffuseMap;
in vec2 fragTexCoord;
out vec4 outColor;
void main() {
    outColor = texture(diffuseMap, fragTexCoord);
}"""

TEXTURE_FRAG = """#version 330 core
uniform sampler2D diffuseMap;
in vec3 fragNormal;
in vec3 fragView;
in vec2 fragTexCoord;
vec3 v, l, n, r, ka, kd, ks, color;
float s, diff, spec;
out vec4 outColor;
void main() {
    v = normalize(fragView);
    l = normalize(vec3(1, 1, 1));
    n = normalize(fragNormal);
    r = reflect(l, n);
    ka = vec3(0.588235, 0.588235, 0.588235);
    kd = vec3(0.588235, 0.588235, 0.588235);
    ks = vec3(0, 0, 0);
    s = 50; // size of the highlights
    diff = max(dot(n, l), 0);
    spec = pow(max(dot(r, v), 0), s); // shape of the specular lobe
    // color = diff * vec3(0, 1, 0); // lambertian model
    color = ka + kd * diff + ks * spec;
    outColor = texture(diffuseMap, fragTexCoord) * vec4(color, 1);
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
        names = ['view', 'projection', 'model', 'diffuseMap']
        loc = {n: GL.glGetUniformLocation(self.shader.glid, n) for n in names}

        GL.glUniformMatrix4fv(loc['view'], 1, True, view)
        GL.glUniformMatrix4fv(loc['projection'], 1, True, projection)
        GL.glUniformMatrix4fv(loc['model'], 1, True, model)

        # texture access setups
        #loc = GL.glGetUniformLocation(self.shader.glid, 'diffuseMap')
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.glid)
        GL.glUniform1i(loc['diffuseMap'], 0)
        self.vertex_array.execute(GL.GL_TRIANGLES)

        # leave clean state for easier debugging
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glUseProgram(0)
