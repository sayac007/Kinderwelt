extends Control
# Keep five independent, native focusable Buttons; draw a continuous illustrated map.
var columns := 1 # Compatibility property used by the existing responsive contract.
const PLACES := [Vector2(.04,.02),Vector2(.54,.20),Vector2(.04,.38),Vector2(.54,.56),Vector2(.29,.78)]
func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_PASS
	custom_minimum_size = Vector2(300,740)
	resized.connect(arrange)
	arrange.call_deferred()
func arrange() -> void:
	var h := 740.0 if size.x<600 else 850.0
	custom_minimum_size.y = h
	for i in range(get_child_count()):
		var child := get_child(i) as Control
		child.position = Vector2(PLACES[i].x*size.x,PLACES[i].y*h)
		child.size = Vector2(size.x*.42,154 if size.x<600 else 170)
	queue_redraw()
func _draw() -> void:
	if size.x<1 or size.y<1: return
	var grass := Color("dceac6")
	var land := PackedVector2Array([Vector2(0,35),Vector2(size.x*.45,0),Vector2(size.x,55),Vector2(size.x,size.y-42),Vector2(size.x*.6,size.y),Vector2(0,size.y-23)])
	draw_colored_polygon(land,grass)
	var route := PackedVector2Array()
	for i in range(5): route.append(Vector2((PLACES[i].x+.21)*size.x,PLACES[i].y*custom_minimum_size.y+75))
	draw_polyline(route,Color("c3a677"),26,true)
	draw_polyline(route,Color("f8e4ba"),18,true)
	for i in range(24):
		var at := Vector2(fmod(i*137.0,size.x),55+fmod(i*83.0,size.y-65))
		draw_line(at,at+Vector2(-3,-7),Color("90ae76"),2,true)
		draw_line(at+Vector2(1,0),at+Vector2(5,-6),Color("90ae76"),2,true)
