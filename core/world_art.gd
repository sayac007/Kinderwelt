extends "res://core/game_art.gd"
# Original scene illustrations. Shared paths and model state stay authoritative.
func _draw() -> void:
	if spec.get("kind") == "world":
		world()
		return
	super._draw()

func world() -> void:
	var scale := minf(size.x/360.0,size.y/170.0)
	draw_set_transform((size-Vector2(360,170)*scale)/2,0,Vector2(scale,scale))
	var world_id: String = spec.world
	draw_style_box(preload("res://core/design.gd").style(Color("eff6eb")),Rect2(8,6,344,156))
	draw_circle(Vector2(300,38),19,Color("edbf60"))
	draw_colored_polygon(PackedVector2Array([Vector2(10,145),Vector2(70,105),Vector2(135,137),Vector2(230,100),Vector2(350,140),Vector2(350,160),Vector2(10,160)]),Color("b7d6a7"))
	match world_id:
		"logic":
			draw_style_box(preload("res://core/design.gd").style(Color("aad7df")),Rect2(115,70,140,90))
			for i in range(7):
				draw_rect(Rect2(90+i*25,92,23,23),Color("b77b42"))
				draw_circle(Vector2(101+i*25,104),2,INK)
			line(Vector2(90,88),Vector2(270,88),INK,4)
			person(Vector2(64,84),26)
			line(Vector2(287,58),Vector2(287,112),INK,4)
			draw_colored_polygon(PackedVector2Array([Vector2(287,58),Vector2(321,69),Vector2(287,80)]),Color("d06a44"))
		"math":
			draw_rect(Rect2(80,60,210,87),Color("b77b42"))
			for i in range(6): draw_rect(Rect2(74+i*37,39,36,36),Color("c65b44") if i%2==0 else Color("fff5d8"))
			for i in range(5): fruit(Vector2(110+i*34,104),15,"apple" if i%2==0 else "pear")
			line(Vector2(80,147),Vector2(80,155),INK,5)
			line(Vector2(285,147),Vector2(285,155),INK,5)
		"language":
			draw_rect(Rect2(74,34,108,113),Color("fffdf3"))
			draw_rect(Rect2(184,34,108,113),Color("fffdf3"))
			line(Vector2(183,34),Vector2(183,147),INK,4)
			fruit(Vector2(124,80),25,"apple")
			for y in [113,126]: line(Vector2(90,y),Vector2(156,y),INK,3)
			person(Vector2(231,78),27)
			line(Vector2(204,126),Vector2(272,126),INK,3)
		"autonomy":
			line(Vector2(75,119),Vector2(130,119),INK,8)
			line(Vector2(130,119),Vector2(130,86),Color("236e96"),9)
			line(Vector2(130,86),Vector2(217,86),Color("236e96"),9)
			for i in range(3): draw_circle(Vector2(220,100+i*12),4,Color("236e96"))
			draw_rect(Rect2(65,53,45,42),Color("236e96"))
			flower(Vector2(245,135),true)
		"social":
			for i in range(3):
				var x := 94+i*85
				draw_rect(Rect2(x-23,73,46,54),Color("f3d4a2"))
				draw_colored_polygon(PackedVector2Array([Vector2(x-31,73),Vector2(x,42),Vector2(x+31,73)]),Color("aa5d4d"))
				person(Vector2(x,125),18)
	draw_set_transform(Vector2.ZERO)

func flower(at: Vector2,grown: bool) -> void:
	line(at,at-Vector2(0,38),Color("456e36"),5)
	line(at-Vector2(0,15),at-Vector2(18,28),Color("456e36"),6)
	if grown:
		for i in range(6): draw_circle(at-Vector2(0,48)+Vector2.from_angle(i*TAU/6)*12,8,Color("d5902d"))
		draw_circle(at-Vector2(0,48),7,Color("674526"))

func bridge() -> void:
	var y := size.y*0.62
	var target := int(spec.target)
	var unit := (size.x-80)/target
	draw_style_box(preload("res://core/design.gd").style(Color("eaf4df")),Rect2(4,4,size.x-8,size.y-8))
	draw_rect(Rect2(38,y-32,size.x-76,65),Color("aad7df"))
	for i in range(3): line(Vector2(50,y+8+i*9),Vector2(size.x-50,y+8+i*9),Color("4b8998"),2)
	for i in range(target): draw_rect(Rect2(40+i*unit,y-28,unit-2,27),INK,false,2)
	var count := 0
	for amount in spec.get("pieces",[]):
		for i in range(int(amount)):
			draw_rect(Rect2(40+(count+i)*unit,y-28,unit-2,27),Color("b77b42"))
			draw_circle(Vector2(40+(count+i+0.5)*unit,y-15),3,INK)
		count += int(amount)
	person(Vector2(lerpf(20.0,size.x-20,crossing) if count==target else 20.0,y-32),22)
	line(Vector2(size.x-20,y-58),Vector2(size.x-20,y-8),INK,3)
	draw_colored_polygon(PackedVector2Array([Vector2(size.x-20,y-58),Vector2(size.x-4,y-48),Vector2(size.x-20,y-38)]),Color("ae5c38"))

func basket() -> void:
	var target := int(spec.target)
	var actual := int(spec.get("amount",0))
	var columns := mini(5,target)
	var spacing := minf((size.x-70)/columns,44)
	var start := Vector2(size.x/2-(columns-1)*spacing/2,45)
	draw_style_box(preload("res://core/design.gd").style(Color("fff5de")),Rect2(4,4,size.x-8,size.y-8))
	for i in range(target):
		var items: Array = spec.get("items",[])
		var kind: String = items[i] if i<items.size() else spec.get("fruit","apple")
		var at := start+Vector2((i%columns)*spacing,int(i/columns)*40)
		if i>=actual and spec.get("any_fruit",false): draw_arc(at,15,0,TAU,24,INK,2,true)
		else: fruit(at,15,kind,i>=actual)
	line(Vector2(20,18),Vector2(27,size.y-12),Color("8c603b"),6)
	line(Vector2(27,size.y-12),Vector2(size.x-27,size.y-12),Color("8c603b"),6)
	line(Vector2(size.x-27,size.y-12),Vector2(size.x-20,18),Color("8c603b"),6)
