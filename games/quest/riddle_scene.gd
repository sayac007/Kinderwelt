extends RefCounted
# Original procedural context illustrations. No answer-atlas texture is drawn.
# The scene illustrates an action/problem; answer pictures remain in the choices.
const Art=preload("res://core/quest/art.gd")
static func box(c: CanvasItem,r: Rect2,color: Color,radius:=12) -> void:
	var style:=StyleBoxFlat.new()
	style.bg_color=color;style.set_corner_radius_all(radius)
	c.draw_style_box(style,r)
static func line(c: CanvasItem,a: Vector2,b: Vector2,color:=Color("40566c"),width:=4.0) -> void:
	c.draw_line(a,b,color,width,true)
static func ellipse(c: CanvasItem,rect: Rect2,color: Color) -> void:
	var points:=PackedVector2Array()
	for i in range(48):points.append(rect.get_center()+Vector2(cos(i*TAU/48),sin(i*TAU/48))*rect.size/2)
	c.draw_colored_polygon(points,color)
static func paint(c: CanvasItem,scene: String,rect: Rect2) -> void:
	var factor:=minf(rect.size.x/320,rect.size.y/240)
	c.draw_set_transform(rect.get_center()-Vector2(160,120)*factor,0,Vector2.ONE*factor)
	box(c,Rect2(9,8,302,204),Color("e9f4f5"),28)
	c.draw_circle(Vector2(265,45),23,Color("f9df8f"))
	Art.text(c,"?",Vector2(265,45),31,Color("755485"))
	match scene:
		"sound":
			box(c,Rect2(45,70,174,100),Color("7971bc"),17)
			for x in [80,180]:
				c.draw_circle(Vector2(x,127),27,Color("343e64"))
				c.draw_circle(Vector2(x,127),15,Color("92e0dc"))
			box(c,Rect2(103,86,54,19),Color("f5d877"),5)
			line(c,Vector2(67,68),Vector2(87,37))
			for x in [234,275]:
				c.draw_circle(Vector2(x,109),6,Color("da867e"))
				line(c,Vector2(x+5,108),Vector2(x+5,80),Color("da867e"))
		"vision":
			box(c,Rect2(50,48,160,126),Color("cb9b6d"),9)
			box(c,Rect2(59,57,142,108),Color("fff7de"),4)
			for i in range(5):
				c.draw_circle(Vector2(85+i*24,112+sin(i)*17),13,[Color("e17f8e"),Color("edb55c"),Color("79b5a0"),Color("6f9bd0"),Color("a181c4")][i])
		"smell":
			box(c,Rect2(105,134,62,47),Color("df9b7b"),10)
			line(c,Vector2(135,134),Vector2(135,85),Color("65a48b"),6)
			for i in range(6):c.draw_circle(Vector2(135,76)+Vector2(cos(i*TAU/6),sin(i*TAU/6))*19,13,Color("d997bf"))
			c.draw_circle(Vector2(135,76),12,Color("ffe19a"))
			for i in range(3):c.draw_arc(Vector2(200+i*13,85-i*8),21,PI*.7,PI*1.3,20,Color("a28dbc"),3,true)
		"taste","bite","food":
			ellipse(c,Rect2(45,122,190,54),Color("a0ccdc"))
			ellipse(c,Rect2(60,129,160,34),Color("fff8e5"))
			c.draw_circle(Vector2(109,111),26,Color("e58973"))
			c.draw_circle(Vector2(154,106),23,Color("efcb68"))
			line(c,Vector2(110,84),Vector2(114,72),Color("718b66"),5)
		"touch","materials":
			box(c,Rect2(45,79,72,74),Color("d6af8c"),5)
			for i in range(4):line(c,Vector2(130+i*19,146),Vector2(140+i*19,88),Color("a68dbf"),8)
			line(c,Vector2(133,96),Vector2(207,96),Color("a68dbf"),8)
			c.draw_arc(Vector2(158,147),42,0,PI,20,Color("6faeab"),5,true)
		"pump","breath","memory","digest","support":
			var colors: Array=[Color("d8858c"),Color("81a8d4"),Color("f1c86c"),Color("96bda4")]
			for i in range(4):
				var p:=Vector2(135,112)+Vector2(cos(i*PI/2),sin(i*PI/2))*55
				c.draw_circle(p,22,colors[i])
				var q:=Vector2(135,112)+Vector2(cos((i+1)*PI/2),sin((i+1)*PI/2))*55
				line(c,p.lerp(q,.3),p.lerp(q,.7),Color("8c79aa"),4)
				c.draw_circle(p.lerp(q,.7),4,Color("8c79aa"))
			Art.text(c,"?",Vector2(135,112),33)
			if scene=="breath":
				for i in range(3):line(c,Vector2(40,89+i*16),Vector2(79,89+i*16),Color("94c5ce"),3)
			if scene=="memory":
				for i in range(3):box(c,Rect2(223,91+i*23,19,16),colors[i],3)
		"shoe":
			c.draw_colored_polygon(PackedVector2Array([Vector2(72,92),Vector2(123,92),Vector2(126,124),Vector2(200,143),Vector2(211,168),Vector2(69,168)]),Color("7d98c0"))
			line(c,Vector2(71,169),Vector2(211,169),Color("fff0d0"),9)
			for i in range(3):line(c,Vector2(124+i*13,126+i*3),Vector2(122+i*13,143+i*3),Color.WHITE,3)
		"motion","safety":
			# Missing wheels create a repair problem, rather than copying a wheel icon.
			line(c,Vector2(74,157),Vector2(119,98),Color("da8d78"),7)
			line(c,Vector2(119,98),Vector2(171,157),Color("da8d78"),7)
			line(c,Vector2(74,157),Vector2(171,157),Color("da8d78"),7)
			line(c,Vector2(119,98),Vector2(192,98),Color("da8d78"),7)
			line(c,Vector2(188,86),Vector2(212,157),Color("829ab6"),6)
			for x in [74,212]:
				c.draw_arc(Vector2(x,157),31,0,TAU,30,Color("abbccc"),2,true)
				Art.text(c,"?",Vector2(x,157),24)
		"tools","force","rope":
			box(c,Rect2(43,137,197,26),Color("ca9c7b"),5)
			line(c,Vector2(70,164),Vector2(64,187),Color("ca9c7b"),9)
			line(c,Vector2(215,164),Vector2(222,187),Color("ca9c7b"),9)
			box(c,Rect2(119,91,44,46),Color("b2c3cf"),4)
			line(c,Vector2(141,53),Vector2(141,89),Color("8c79aa"),3)
			line(c,Vector2(130,77),Vector2(141,88),Color("8c79aa"),3)
			line(c,Vector2(151,77),Vector2(141,88),Color("8c79aa"),3)
		"electric","light":
			box(c,Rect2(64,81,60,74),Color("8b9ebb"),13)
			box(c,Rect2(118,100,32,35),Color("637997"),4)
			c.draw_colored_polygon(PackedVector2Array([Vector2(150,102),Vector2(237,62),Vector2(237,172),Vector2(150,133)]),Color("ffe5a2"))
			for i in range(3):line(c,Vector2(37,89+i*21),Vector2(53,89+i*21),Color("d6aa69"),3)
		"growth","life":
			box(c,Rect2(73,116,132,60),Color("d89e7e"),14)
			ellipse(c,Rect2(73,102,132,39),Color("866c62"))
			for i in range(6):c.draw_circle(Vector2(89+i*20,117+(i%2)*5),3,Color("be9b7c"))
			Art.text(c,"?",Vector2(139,78),37,Color("72a18a"))
			line(c,Vector2(226,96),Vector2(226,161),Color("97b6c7"),5)
		"cold","heat","water","cleaning":
			box(c,Rect2(68,74,111,93),Color("fff6dd"),11)
			line(c,Vector2(82,167),Vector2(166,167),Color("9ab3c1"),4)
			c.draw_arc(Vector2(178,111),24,-PI/2,PI/2,20,Color("fff6dd"),9,true)
			box(c,Rect2(222,70,13,76),Color("97b7cc"),5)
			c.draw_circle(Vector2(228,148),15,Color("df9c90") if scene=="heat" else Color("91b8d4"))
			Art.text(c,"?",Vector2(121,118),35)
		"navigation","landscape","weather":
			box(c,Rect2(56,55,156,125),Color("fcf5df"),8)
			var path:=PackedVector2Array([Vector2(75,153),Vector2(111,119),Vector2(92,91),Vector2(173,76),Vector2(191,126)])
			c.draw_polyline(path,Color("b294b0"),7,true)
			for p in path:c.draw_circle(p,6,Color("76aaa3"))
			Art.text(c,"?",Vector2(188,151),29)
		"rest":
			box(c,Rect2(49,111,178,53),Color("9e94c3"),10)
			box(c,Rect2(50,92,61,31),Color("fff4dd"),10)
			line(c,Vector2(49,83),Vector2(49,185),Color("ba977d"),9)
			line(c,Vector2(227,125),Vector2(227,185),Color("ba977d"),9)
		"brush":
			line(c,Vector2(69,151),Vector2(210,95),Color("8baec6"),18)
			for i in range(6):line(c,Vector2(176+i*8,103-i*3),Vector2(169+i*8,83-i*3),Color("fff9e7"),6)
		_:
			Art.text(c,"?",Vector2(145,112),62,Color("9b82bc"))
	c.draw_set_transform(Vector2.ZERO)
