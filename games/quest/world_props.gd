extends RefCounted
const Art=preload("res://core/quest/art.gd")
const SQUIRREL=preload("res://assets/quest/squirrel.png")
static func rounded(canvas: CanvasItem,rect: Rect2,color: Color,radius: int=12,border:=Color("604854")) -> void:
	var style:=StyleBoxFlat.new();style.bg_color=color;style.border_color=border
	style.set_corner_radius_all(radius);style.set_border_width_all(2)
	canvas.draw_style_box(style,rect)
static func branch(canvas: CanvasItem,c: Vector2,phase: float) -> void:
	canvas.draw_line(c+Vector2(-95,40),c+Vector2(65,40),Color("69442c"),18,true)
	canvas.draw_line(c+Vector2(-90,37),c+Vector2(59,37),Color("c7924a"),7,true)
	canvas.draw_texture_rect(SQUIRREL,Rect2(c+Vector2(-99,-46+sin(phase*2)*2),Vector2(60,72)),false)
	# A large, recognizable acorn is the actual task target.
	canvas.draw_circle(c+Vector2(0,5),28,Color("c77e36"))
	canvas.draw_circle(c+Vector2(-7,0),17,Color("e8b664"))
	rounded(canvas,Rect2(c+Vector2(-34,-24),Vector2(68,23)),Color("855138"),11)
	canvas.draw_line(c+Vector2(0,-23),c+Vector2(5,-38),Color("734935"),6,true)
static func chest(canvas: CanvasItem,c: Vector2,solved: bool) -> void:
	canvas.draw_circle(c,43,Color(.65,.95,1,.14))
	rounded(canvas,Rect2(c+Vector2(-39,-30),Vector2(78,63)),Color("8b513d"),10)
	rounded(canvas,Rect2(c+Vector2(-38,-29),Vector2(76,25)),Color("bf8551"),12)
	for x in [-25,25]:rounded(canvas,Rect2(c+Vector2(x-5,-28),Vector2(10,59)),Color("f5c464"),3)
	if solved:canvas.draw_line(c+Vector2(-36,-33),c+Vector2(32,-51),Color("e8b45d"),14,true)
static func wreck(canvas: CanvasItem,c: Vector2) -> void:
	canvas.draw_colored_polygon(PackedVector2Array([c+Vector2(-73,-13),c+Vector2(66,-13),c+Vector2(40,28),c+Vector2(-43,24)]),Color("49696b"))
	canvas.draw_line(c+Vector2(-17,-13),c+Vector2(-33,-90),Color("698780"),7,true)
	canvas.draw_colored_polygon(PackedVector2Array([c+Vector2(-33,-85),c+Vector2(-22,-29),c+Vector2(29,-36)]),Color("829b86"))
	for x in [-35,0,35]:canvas.draw_circle(c+Vector2(x,1),7,Color("203e54"))
static func city_prop(canvas: CanvasItem,c: Vector2,index: int) -> void:
	match index%3:
		0: # Bus shelter, with task clue on its stop sign.
			canvas.draw_line(c+Vector2(0,-46),c+Vector2(0,57),Color("45647c"),6,true)
			rounded(canvas,Rect2(c+Vector2(-47,5),Vector2(94,9)),Color("c68c58"),3)
			for x in [-40,40]:canvas.draw_line(c+Vector2(x,12),c+Vector2(x,48),Color("45647c"),5,true)
			rounded(canvas,Rect2(c+Vector2(-55,-53),Vector2(110,14)),Color("65bfc3"),7)
			canvas.draw_line(c+Vector2(65,-35),c+Vector2(65,45),Color("45647c"),4,true)
			rounded(canvas,Rect2(c+Vector2(53,-37),Vector2(25,31)),Color("4b89b3"),7)
			rounded(canvas,Rect2(c+Vector2(58,-30),Vector2(15,16)),Color("fff2bd"),3)
			for x in [61,70]:canvas.draw_circle(c+Vector2(x,-13),2,Color("334e6a"))
		1: # Walk/drive beneath the arch to find a task.
			canvas.draw_arc(c+Vector2(0,37),73,PI,TAU,32,Color("8d8cb1"),22,true)
			canvas.draw_arc(c+Vector2(0,37),73,PI,TAU,32,Color("c6c0d6"),14,true)
		2:
			rounded(canvas,Rect2(c+Vector2(-42,-48),Vector2(84,99)),Color("de927c"),8)
			for x in [-24,12]:rounded(canvas,Rect2(c+Vector2(x,-30),Vector2(17,23)),Color("abedf0"),3)
static func beacon(canvas: CanvasItem,c: Vector2,phase: float) -> void:
	canvas.draw_circle(c+Vector2(0,39),43,Color(.3,.25,.47,.25))
	rounded(canvas,Rect2(c+Vector2(-32,17),Vector2(64,21)),Color("c2c2e6"),9)
	canvas.draw_line(c+Vector2(0,18),c+Vector2(0,-41),Color("e4e3ff"),6,true)
	canvas.draw_arc(c+Vector2(0,-42),16,.25,PI-.25,16,Color("f9d870"),4,true)
	canvas.draw_circle(c+Vector2(0,-42),4+sin(phase*2),Color("8df1f5"))
static func clue(canvas: CanvasItem,c: Vector2,solved: bool,object: String,index: int) -> void:
	canvas.draw_circle(c,31,Color("fff5c7") if solved else Color("fffcf1"))
	canvas.draw_arc(c,31,0,TAU,32,Color("a67638"),2,true)
	if solved:Art.star(canvas,c,21,Color("efa923"))
	elif object=="?":Art.text(canvas,"?",c,34,Color("76528c"))
	else:Art.object(canvas,object,Rect2(c-Vector2(23,23),Vector2(46,46)))
	canvas.draw_circle(c+Vector2(28,27),12,Color("fff8d9"))
	Art.text(canvas,str(index+1),c+Vector2(28,27),13)
