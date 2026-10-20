extends Control
const Art = preload("res://core/quest/art.gd")
var value: Variant
var kind := ""
func _ready() -> void: mouse_filter = MOUSE_FILTER_IGNORE
func _draw() -> void:
	var rect := Rect2(Vector2(9,8),size-Vector2(18,16))
	if value is String and Art.REGIONS.has(value):
		Art.object(self,value,rect)
	elif kind=="size":
		var scale_factor: float = {"small":.45,"medium":.7,"large":1.0}.get(value,1.0)
		rect.position.y += rect.size.y*(1-scale_factor)
		rect.size.y *= scale_factor
		Art.object(self,"tree",rect)
	elif kind=="syllables":
		for i in range(int(value)):
			var x := size.x*(i+1)/(int(value)+1)
			draw_circle(Vector2(x,size.y/2),6,Color("345c7c"))
	elif value in ["left","right"]:
		Art.text(self,"←" if value=="left" else "→",size/2,36)
	else:
		var caption := str(int(value)) if value is float or value is int else str(value)
		Art.text(self,caption,size/2,24 if caption.length()>2 else 36)
