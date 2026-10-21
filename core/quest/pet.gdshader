shader_type canvas_item;
uniform float phase = 0.0;
uniform bool walking = false;
uniform bool still = false;
uniform vec2 sprite_size = vec2(140.0, 210.0);

void vertex() {
	if (!still) {
		// The approved image has the curled tail on its left and paws below .77.
		float tail = (1.0-smoothstep(0.18,0.39,UV.x))*smoothstep(0.08,0.25,UV.y)*(1.0-smoothstep(0.65,0.84,UV.y));
		VERTEX.x += sin(phase*2.5)*tail*sprite_size.x*0.022;
		if (walking) {
			float paws = smoothstep(0.76,0.96,UV.y);
			float step_phase = phase*9.0+floor(UV.x*4.0)*3.14159265;
			VERTEX.y -= max(0.0,sin(step_phase))*paws*sprite_size.y*0.024;
			VERTEX.x += cos(step_phase)*paws*sprite_size.x*0.018;
		}
	}
}
