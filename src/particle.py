import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np
import sys, random

from loaders import load_textured
from node import Node
from cubemap import Cubemap
from shader import Shader
from vertex_array import VertexArray

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

MAX_PARTICLES = 500
SPEED_PARTICLES = 2.0
XSPEED = 0.0
YSPEED = 0.0
ZOOM = -30.0
LOOP = 0
DELAY = 0

colors_p = [[(1.0,0.5,0.5),(1.0,0.75,0.5),(1.0,1.0,0.5),(0.75,1.0,0.5)],
			[(0.5,1.0,0.5),(0.5,1.0,0.75),(0.5,1.0,1.0),(0.5,0.75,1.0)],
			[(0.5,0.5,1.0),(0.75,0.5,1.0),(1.0,0.5,1.0),(1.0,0.5,0.75)]]

class Particle:
	def __init__(self, file):

		self.ACTIVE = 1 
		self.LIFE = 0.0
		self.FADE = 0.0

		self.R = 0.0
		self.G = 0.0
		self.B = 0.0

		self.X = 0.0
		self.Y = 0.0
		self.Z = 0.0

		self.Xi = 0.0
		self.Yi = 0.0
		self.Zi = 0.0

		self.Xg = 0.0 #X gravity
		self.Yg = 0.0 #Y gravity
		self.Zg = 0.0 #Z gravity

		self.glid = glGenTextures(1)
		GL.glBindTexture(GL_TEXTURE_2D, self.glid)
		try:
			self.__load(file)
			
			GL.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
			GL.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
			GL.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
			GL.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
			GL.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
			GL.glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
			GL.glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
		except FileNotFoundError:
			print("ERROR: unable to load texture file %s" & file)
		GL.glBindTexture(GL_TEXTURE_2D, 0)

	def __load(self, file):
		particle_tex = np.array(Image.open(file))

		Gl.glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		GL.glTexImage2D(GL_TEXTURE_2D, 0, 3, particle_tex[1], particle_tex[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, particle_tex)

	def draw(self, projection, view, model, color_shader=None, win=None, **param):

		for i in range(NB_PARTICLES):
			Particle = particle("res/glitter_texture.jpg")
			particleList.append(Particle)

		

	def __del__(self):
		GL.glDeleteTextures(self.glid)





class ParticleCloud:
	def __init__(self, file):

		for i in range(NB_PARTICLES):
			particleList[i].LIFE= 1.0
			particleList[i].FADE= float(random.randrange(0,100))/1000.0+0.003

			particleList[i].R = colors_p[i*(12/1000)][0]
			particleList[i].G = colors_p[i*(12/1000)][1]
			particleList[i].B = colors_p[i*(12/1000)][2]

			particleList[i].Xi = (float(random.randrange(0,100)%50)-26.0)*10.0
			particleList[i].Yi = (float(random.randrange(0,100)%50)-26.0)*10.0
			particleList[i].Zi = (float(random.randrange(0,100)%50)-26.0)*10.0
		
			particleList[i].Xg = 0.0
			particleList[i].Yg = -0.8
			particleList[i].Zg = 0.0






#-----------------------
#class ParticleCloud:
	def __init__():
		self.particleList = []
		for _ in NB_PARTICLES:
			self.particleList.append(Particle())

	def firstUnusedParticle():
		
		for i in range(lastUsedParticle, len(particleList)):
			if particleList[i].life == 0.0:
				lastUsedParticle = i
				return i

		for i in particleList:
			if particleList[i].life == 0.0:
				lastUsedParticle = i
				return i

		lastUsedParticle = 0
		return 0

	def respawnParticle( particle, offset):
		Particle = particle
		random = random()
		rColor = 0.5 + random()
		Particle.position = random + offset
		Particle.color = (rColor,rColor, rColor, 1.0)
		Particle.life = 1.0
		Particle.velocity = random() * 0.1


	def draw():
		for i in particleList:
			particleList[i].draw()