extends Control
func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO,size),Color("19384f"))
	preload("res://core/quest/scenery.gd").paint(self,"moon",Rect2(Vector2.ZERO,size),Color(.65,.75,1))
	for point in [Vector2(110,95),Vector2(880,100),Vector2(740,400),Vector2(245,390)]:
		draw_circle(point,18,Color("ffd168"))
func _ready() -> void:
	var figure:=preload("res://core/quest/hero.gd").new()
	figure.person="wanja";figure.costume="astronaut";figure.selected=true
	figure.reduced_motion=true;figure.position=Vector2(400,35);figure.size=Vector2(230,430)
	add_child(figure)
