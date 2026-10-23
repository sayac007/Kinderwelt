extends Control
var phase := 0.0
var facing := 1.0
func _ready() -> void: mouse_filter=MOUSE_FILTER_IGNORE
func _draw() -> void:
	draw_set_transform(Vector2(size.x/2,0),0,Vector2(facing,1))
	oval_shadow(Vector2(0,61),Vector2(78,10),Color(0,0,0,.2))
	var body:=StyleBoxFlat.new();body.bg_color=Color("faad39");body.border_color=Color("854d49")
	body.set_border_width_all(2);body.set_corner_radius_all(20)
	draw_style_box(body,Rect2(-76,20,152,38))
	var shine:=StyleBoxFlat.new();shine.bg_color=Color("ffe196");shine.set_corner_radius_all(8)
	draw_style_box(shine,Rect2(-64,24,114,9))
	# Open-top car: the chosen character remains visible behind this foreground.
	draw_line(Vector2(33,24),Vector2(23,-12),Color("d8ffff"),5,true)
	draw_line(Vector2(23,-12),Vector2(39,-10),Color("94d9ed"),4,true)
	for x in [-46,46]:
		draw_circle(Vector2(x,55),17,Color("273d53"))
		draw_circle(Vector2(x,55),10,Color("d1e5ed"))
		for spoke in range(4):
			var a:=phase+spoke*PI/2
			draw_line(Vector2(x,55),Vector2(x,55)+Vector2(cos(a),sin(a))*8,Color("577990"),2,true)
	draw_circle(Vector2(66,35),7,Color("fff7cc"))
	draw_circle(Vector2(-67,35),4,Color("ef6364"))
	draw_set_transform(Vector2.ZERO)
func oval_shadow(center: Vector2,radius: Vector2,color: Color) -> void:
	draw_set_transform(Vector2(size.x/2,0),0,Vector2(facing,1))
	var points:=PackedVector2Array()
	for i in range(32):points.append(center+Vector2(cos(i*TAU/32),sin(i*TAU/32))*radius)
	draw_colored_polygon(points,color)
