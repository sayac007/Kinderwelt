extends Button
const Scenery=preload("res://core/quest/scenery.gd")
var scenery := "mountains"
var chosen := false
func _draw() -> void:
	var rect:=Rect2(Vector2(8,8),Vector2(size.x-16,size.y-64))
	Scenery.paint(self,"mountains" if scenery=="auto" else scenery,rect)
	if scenery=="auto":
		preload("res://core/quest/art.gd").text(self,"↻",rect.get_center(),42,Color.WHITE)
	if chosen:
		draw_circle(Vector2(size.x-27,27),16,Color("fff5c5"))
		preload("res://core/quest/art.gd").text(self,"✓",Vector2(size.x-27,27),23)
