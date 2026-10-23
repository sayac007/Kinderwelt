shader_type canvas_item;
uniform float phase = 0.0;
uniform bool walking = false;
uniform bool still = false;
uniform bool squirrel = false;
uniform bool human = false;
uniform vec4 atlas_rect = vec4(0.0,0.0,1.0,1.0);
uniform sampler2D frame_mask : filter_nearest, repeat_disable;
uniform float mask_id=0.0;
varying vec4 sprite_tint;
uniform vec2 sprite_size = vec2(140.0, 210.0);

void vertex() {
	sprite_tint=COLOR;
	if (!still) {
		// The approved image has the curled tail on its left and paws below .77.
		float tail = (1.0-smoothstep(0.18,0.39,UV.x))*smoothstep(0.08,0.25,UV.y)*(1.0-smoothstep(0.65,0.84,UV.y));
		if (squirrel) { tail=smoothstep(0.55,0.83,UV.x)*(1.0-smoothstep(0.74,0.93,UV.y)); }
		if (human) { tail=0.0; }
		VERTEX.x += sin(phase*2.5)*tail*sprite_size.x*0.022;
		if (walking) {
			float paws = smoothstep(0.76,0.96,UV.y);
			float step_phase = phase*9.0+floor(UV.x*((squirrel || human) ? 2.0 : 4.0))*3.14159265;
			VERTEX.y -= max(0.0,sin(step_phase))*paws*sprite_size.y*0.024;
			VERTEX.x += cos(step_phase)*paws*sprite_size.x*0.018;
		}
	}
}

void fragment() {
	vec2 at=atlas_rect.xy+UV*atlas_rect.zw;
	COLOR=texture(TEXTURE,at)*sprite_tint;
	if (mask_id>0.0 && abs(texture(frame_mask,at).r*255.0-mask_id)>0.25) { COLOR=vec4(0.0); }
}
