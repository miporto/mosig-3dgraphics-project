#inspired from c++ tutorial 
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np
import sys, random

from loaders import load_textured
from node import Node
from cubemap import Cubemap
from shader import Shader
from vertex_array_p import VertexArrayP
from tranform import vec2,vec4

VEC_Particle_SHAD = """#version 330 core 
layout (location = 0) in vec4 vertex;
out vec TexCoord;
out vec4 ParticleColor;

uniform mat4 modelviewprojection;
uniform vec2 offset;
uniform vec4 color;

void main() {
	float scale = 10.0f;
    TexCoord = vertex.zw;
    ParticleColor = color;
    gl_Position = modelviewprojection * vec4((vertex.xy * scale)+ offset ,0.0, 1.0);
}
"""

FRAG_Particle_SHAD = """#version 330 core // changeee
in vec2 TexCoord;
in vec4 ParticleColor;
out vec4 FragColor;

uniform sampler2D sprite;

void main() {
    FragColor = (texture(sprite, TexCoord) * ParticleColor);
}
"""


class Particle():
	def __init__():
		self.pos = vec((0,0))
		self.vel = vec((0,0))
		self.col = vec((1,1,1,1))
		self.life = 0.0

particle_vertices = np.array(
		(0.0, 1.0, 0.0, 1.0,
        1.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 0.0,

        0.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 0.0, 1.0, 0.0),'f')


class ParticleGenerator():
	def __init__(nb_p):
		
		self.file = 'res/glitter_texture.jpg' #the texture of the Particle
		self.vertex_array = VertexArrayP(particle_vertices)
		self.nb_particles = nb_p
		self.particleList = []
		self.lastUsedParticle = 0
		for i in range(nb_particles):
			particleList.append(Particle())


	def update(dt, newParticles, offset):
		for i in range(newParticles):
			unusedParticle = FirstUnusedParticle()
			respawnParticle(self.particleList[unusedParticle], offset)

		for particle in self.particleList:
			particle.life -= dt
			if particle.life > 0.0:
				particle.pos -= particle.vel * dt
				particle.col[-1] -= dt * 2.5

	def FirstUnusedParticle():
		for i in range(self.lastUsedParticle : self.nb_particles):
			if particleList[i].life	<= 0.0:
				self.lastUsedParticle = i
				return i	

		for i in range(self.lastUsedParticle):
			if particleList[i].life	<= 0.0:
				self.lastUsedParticle = i
				return i

		self.lastUsedParticle = 0
		return 0
	def respawnParticle(Particle, offset):
		random = ( random.random()*100 - 50 )/10.0
		rColor = 0.5 + ( random.random()*100 )/10.0

		Particle.pos = random + offset
		Particle.col = vec((rColor,rColor,rColor,1.0))
		Particle.life = 1.0
		Particle.vel = random.random()* 10 * 0.1

class ParticleGen():
	 def __init__(self, attributes=[particle_vertices]):
        self.shader = Shader(VEC_Particle_SHAD, FRAG_Particle_SHAD)
        self.vertex_array = VertexArray(attributes)
        self.particleGroup = ParticleGenerator(500)

    def draw(self, projection, view, model, color_shader=None, win=None, **param):
        """ Draw object """
        #GL.glDepthFunc(GL.GL_LEQUAL)
        #GL.glDepthMask(GL.GL_FALSE)
        GL.glBlendFunc(GL_SRC_ALPHA, GL_ONE)
        GL.glUseProgram(self.shader.glid)

        offset_loc = GL.glGetUniformLocation(self.shader.glid, 'offset')
        color_loc = GL.glGetUniformLocation(self.shader.glid, 'color')
        for particle in self.particleGroup.particleList:
        	if particle.life > 0.0:
        		GL.glUniform2fv(offset_loc,1,particle.pos)
        		GL.glUniform2fv(color_loc,1,particle.col)


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
	