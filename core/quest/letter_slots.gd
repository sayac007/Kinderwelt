extends RefCounted
## A fixed cell per written position: underscores and letters never slide around.
const Art = preload("res://core/quest/art.gd")
static func cells(value: String,rect: Rect2) -> Array[Rect2]:
	var result: Array[Rect2]=[]
	if value.is_empty(): return result
	var width:=minf(28,rect.size.x/value.length())
	var left:=rect.get_center().x-width*value.length()/2
	for i in range(value.length()): result.append(Rect2(Vector2(left+i*width,rect.position.y),Vector2(width,rect.size.y)))
	return result
static func paint(canvas: CanvasItem,value: String,rect: Rect2) -> void:
	var positions:=cells(value,rect)
	for i in range(positions.size()):
		var px:=mini(25,floori(positions[i].size.x*.9))
		Art.text(canvas,value[i],positions[i].get_center(),px,Color("63717c") if value[i]=="_" else Art.INK)
