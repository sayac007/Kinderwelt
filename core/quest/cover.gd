extends Control
var track := "meadow"
const Tracks = preload("res://core/quest/tracks.gd")
func _ready() -> void: mouse_filter = Control.MOUSE_FILTER_IGNORE
func _draw() -> void:
	var data: Dictionary = Tracks.ITEMS[track]
	var k := minf(size.x/150,size.y/112)
	draw_set_transform(Vector2((size.x-150*k)/2,0),0,Vector2(k,k))
	var ink := Color("354b53")
	var paper := Color(data.color)
	var shape := PackedVector2Array([Vector2(5,12),Vector2(128,3),Vector2(145,94),Vector2(20,109)])
	draw_colored_polygon(shape,paper)
	draw_polyline(shape+PackedVector2Array([shape[0]]),ink,2.5,true)
	var index: int = Tracks.ITEMS.keys().find(track)
	for i in range(5):
		var y := 33+i*11
		draw_line(Vector2(25,y+sin(index+i)*9),Vector2(116,y+sin(index+i+1)*9),paper.lightened(.25),3,true)
	var center := Vector2(76,53)
	match data.icon:
		"gear":
			draw_circle(center,25,ink)
			for i in range(8): draw_line(center+Vector2.from_angle(i*TAU/8)*19,center+Vector2.from_angle(i*TAU/8)*31,ink,8,true)
			draw_circle(center,12,paper)
		"moon":
			draw_circle(center,28,ink)
			draw_circle(center+Vector2(14,-10),22,paper)
			for i in range(3): draw_circle(Vector2(33+i*37,21+i%2*56),3,ink)
		"leaf":
			draw_line(center+Vector2(0,30),center+Vector2(0,-24),ink,4,true)
			for i in [-1,1]:
				draw_colored_polygon(PackedVector2Array([center,center+Vector2(i*28,-24),center+Vector2(i*26,0),center+Vector2(0,15)]),ink)
		"drop":
			draw_colored_polygon(PackedVector2Array([center+Vector2(0,-31),center+Vector2(-20,2),center+Vector2(-16,18),center+Vector2(0,25),center+Vector2(16,18),center+Vector2(20,2)]),ink)
		"sun":
			draw_circle(center,19,ink)
			for i in range(8): draw_line(center+Vector2.from_angle(i*TAU/8)*25,center+Vector2.from_angle(i*TAU/8)*33,ink,3,true)
	# Printed track marks vary as well as colors and the central motif.
	for i in range(index+1): draw_circle(Vector2(25+i*9,94),2,ink)
	draw_set_transform(Vector2.ZERO)
