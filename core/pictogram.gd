extends Control
var kind := "star"
var lit := false

func _draw() -> void:
	var c := size / 2
	var s := minf(size.x, size.y) * 0.32
	var ink := Color("ffdc78") if lit else Color("c7edff")
	match kind:
		"bridge":
			draw_line(c + Vector2(-s,s/2), c + Vector2(s,s/2), ink, 10)
			for x in [-1,0,1]: draw_line(c+Vector2(x*s,-s/2),c+Vector2(x*s,s),ink,8)
		"dots":
			for x in [-1,0,1]: draw_circle(c+Vector2(x*s*0.8,0),s*0.25,ink)
		"book":
			draw_rect(Rect2(c-Vector2(s,s*0.7),Vector2(s*2,s*1.4)),ink,false,8)
			draw_line(c-Vector2(0,s*0.7),c+Vector2(0,s*0.7),ink,6)
		"people":
			for x in [-1,1]:
				draw_circle(c+Vector2(x*s*0.55,-s*0.45),s*0.3,ink)
				draw_line(c+Vector2(x*s*0.55,0),c+Vector2(x*s*0.55,s),ink,12)
		_:
			var points := PackedVector2Array()
			for i in range(10):
				var a := i * PI / 5 - PI/2
				points.append(c+Vector2(cos(a),sin(a))*s*(1.0 if i%2==0 else 0.45))
			draw_colored_polygon(points,ink)
