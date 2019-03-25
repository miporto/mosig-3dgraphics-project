#!/usr/bin/env python3
"""
Viewer class & window management
"""
# Python built-in modules
from itertools import cycle

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL

from shader import Shader
from trackball import GLFWTrackball
from transform import identity

# ------------  simple color fragment shader demonstrated in Practical 1 ------
COLOR_VERT = """#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
out vec3 fragNormal;
out vec3 fragView;

void main() {
    gl_Position = projection * view * model * vec4(position, 1);
    //fragNormal = normal; // fixed light
    // light 'rotates' with camera movement
    fragNormal = transpose(inverse(mat3(view * model))) * normal;
    fragView = normalize((view * model * vec4(position, 1)).xyz);
}"""


COLOR_FRAG = """#version 330 core
in vec3 fragNormal;
in vec3 fragView;
vec3 v;
vec3 l;
vec3 n;
vec3 r;
vec3 ka;
vec3 kd;
vec3 ks;
vec3 color;
float s;
float diff;
float spec;
out vec4 outColor;
void main() {
    v = normalize(fragView);
    l = normalize(vec3(0, 0, 1));
    n = normalize(fragNormal);
    r = reflect(l, n);
    ka = vec3(0, 0, 1);
    kd = vec3(1, 0.5, 0.5);
    ks = vec3(1, 0, 0);
    s = 50; // size of the highlights
    diff = max(dot(n, l), 0);
    spec = pow(max(dot(r, v), 0), s); // shape of the specular lobe
    //color = diff * vec3(0, 1, 0); // lambertian model
    color = ka + kd * diff + ks * spec;
    outColor = vec4(color, 1);
}"""

class Viewer:
    """ GLFW viewer window, with classic initialization & graphics loop """

    def __init__(self, width=800, height=600):

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)
        GL.glEnable(GL.GL_DEPTH_TEST)         # depth test now enabled (TP2)
        GL.glEnable(GL.GL_CULL_FACE)          # backface culling enabled (TP2)

        # compile and initialize shader programs once globally
        self.color_shader = Shader(COLOR_VERT, COLOR_FRAG)

        # initially empty list of object to draw
        self.drawables = []

        # initialize trackball
        self.trackball = GLFWTrackball(self.win)

        # cyclic iterator to easily toggle polygon rendering modes
        self.fill_modes = cycle([GL.GL_LINE, GL.GL_POINT, GL.GL_FILL])

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            # clear draw buffer and depth buffer (<-TP2)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            winsize = glfw.get_window_size(self.win)
            view = self.trackball.view_matrix()
            projection = self.trackball.projection_matrix(winsize)

            # draw our scene objects
            for drawable in self.drawables:
                drawable.draw(projection, view, identity(),
                              color_shader=self.color_shader, win=self.win)

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def add(self, *drawables):
        """ add objects to draw in this window """
        self.drawables.extend(drawables)

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)
            if key == glfw.KEY_W:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fill_modes))
