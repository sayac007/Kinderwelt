extends Control
const Art = preload("res://core/quest/art.gd")
var value: Variant
var kind := ""
var caption := ""
var slot_pattern := ""
func _ready() -> void: mouse_filter = MOUSE_FILTER_IGNORE
func _draw() -> void:
	var rect := Rect2(Vector2(9,8),size-Vector2(18,16))
	if kind=="word" and not slot_pattern.is_empty():
		preload("res://core/quest/letter_slots.gd").paint(self,slot_pattern,rect)
	elif kind=="dual_pattern":
		var pair:=str(value).split(":")
		Art.object(self,pair[0],Rect2(rect.position,Vector2(rect.size.x,rect.size.y-22)))
		Art.text(self,pair[1],Vector2(size.x/2,size.y-13),20)
	elif value is String and Art.has_object(value):
		if kind in ["discovery","rhyme","reasoning_choice"]: rect.size.y-=20
		Art.object(self,value,rect)
		if kind in ["discovery","rhyme","reasoning_choice"]:
			var px := 14
			while px>10 and Art.font().get_string_size(caption,HORIZONTAL_ALIGNMENT_LEFT,-1,px).x>size.x-8: px-=1
			var shown := caption
			while shown.length()>2 and Art.font().get_string_size(shown,HORIZONTAL_ALIGNMENT_LEFT,-1,px).x>size.x-8:
				shown=shown.left(shown.length()-2)+"…"
			Art.text(self,shown,Vector2(size.x/2,size.y-13),px)
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
		var px:=24 if caption.length()>2 else 36
		while px>10 and Art.font().get_string_size(caption,HORIZONTAL_ALIGNMENT_LEFT,-1,px).x>size.x-12: px-=1
		Art.text(self,caption,size/2,px)
