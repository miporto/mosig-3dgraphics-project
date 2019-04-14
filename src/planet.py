from transform import translate, scale,vec ,quaternion_from_euler
from loaders import load_textured
from node import *
from keyframe import KeyFrameControlNode

TEXTURE_FRAG_BLUR = """#version 330 core
uniform sampler2D diffuseMap;
in vec2 fragTexCoord;

out vec4 outColor;

uniform float weight[5] = float[](0.227027, 0.1945946, 0.1216216, 0.054054, 0.016216);

void main() {

    vec2 tex_offset = 1.0/ textureSize(diffuseMap, 0);
    vec3 result = texture(diffuseMap , fragTexCoord ).rgb * weight[0];

    for(int i = 1 ; i < 6; i++){
        result += texture(diffuseMap, fragTexCoord + vec2(tex_offset.x * i,0.0)).rgb * weight[i];
        result += texture(diffuseMap , fragTexCoord - vec2(tex_offset.x * i,0.0)).rgb * weight[i];
    }
    outColor = vec4(result,1.0); // with blur
     //outColor = texture(diffuseMap, fragTexCoord);
}"""


class Planet(Node):
    """Keyboard movable spaceship"""
    def __init__(self):
    	super().__init__(transform = scale(0.03,0.03,0.03) )
    	self.add(*load_textured('res/satellite/Mars 2K.obj',TEXTURE_FRAG_BLUR))    

class PlanetLoader():
	def __init__(self):

		planet = Planet()

		rotate_planet = {0: quaternion_from_euler(0,0,0) ,10:quaternion_from_euler(0,15,0),20:quaternion_from_euler(0,90,0)}
		keynode = KeyFrameControlNode({0:vec(.8,.8,-.9)},rotate_planet,{0:1, 2:1})
		keynode.add(planet)
		self.satellite = keynode

	def get_planet(self):
		return self.satellite
