shader_type canvas_item;
uniform vec4 region = vec4(0.0, 0.0, 1.0, 1.0);
varying vec4 tint;
void vertex() { tint = COLOR; }
void fragment() {
	vec4 pixels = texture(TEXTURE, region.xy + UV * region.zw);
	float edge = 1.0 - smoothstep(0.493, 0.5, distance(UV, vec2(0.5)));
	COLOR = pixels * tint;
	COLOR.a *= edge;
}
