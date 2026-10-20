extends "res://core/game_art.gd"
# Original vector scenes. Identity and quantity use shapes, not colour alone.
func _draw() -> void:
	super._draw()
	if spec.get("kind") not in ["story", "story_slot", "experiment", "setting", "village", "plan", "adult", "test", "previous", "forward"]: return
	var factor := minf(size.x / 300.0, size.y / 150.0)
	draw_set_transform((size - Vector2(300,150) * factor) / 2, 0, Vector2(factor,factor))
	draw_style_box(preload("res://core/design.gd").style(Color("d4e8d9") if spec.get("selected",false) else Color("f1f5e9")),Rect2(4,4,292,142))
	match spec.kind:
		"story": story(spec.card.scene, int(spec.card.step))
		"story_slot":
			draw_rect(Rect2(12,12,276,126),INK,false,3)
			for i in range(int(spec.get("ordinal",1))): draw_circle(Vector2(125+i*13,125),4,GOLD)
			if spec.has("card"): story(spec.card.scene,int(spec.card.step))
		"experiment": experiment_view()
		"setting":
			draw_setting(spec.experiment, int(spec.control), int(spec.value))
			for i in range(int(spec.value)): draw_circle(Vector2(118+i*18,130),5,GOLD)
			if int(spec.value)==0: draw_arc(Vector2(145,130),5,0,TAU,12,INK,2)
		"village": village()
		"plan":
			plan(spec.gives)
			plan_detail(spec.get("style", ""))
		"adult":
			person(Vector2(115,78),30)
			person(Vector2(175,88),20)
			draw_rect(Rect2(175,20,65,32),INK,false,3)
			for i in range(3): draw_circle(Vector2(190+i*15,35),3,GOLD)
		"test", "forward":
			draw_colored_polygon(PackedVector2Array([Vector2(125,40),Vector2(185,75),Vector2(125,110)]),GOLD)
		"previous":
			draw_colored_polygon(PackedVector2Array([Vector2(175,40),Vector2(115,75),Vector2(175,110)]),GOLD)
	draw_set_transform(Vector2.ZERO)

func sun(at: Vector2, radius := 17.0) -> void:
	draw_circle(at,radius,GOLD)
	for i in range(8):
		var ray := Vector2.from_angle(i*TAU/8)
		line(at+ray*(radius+4),at+ray*(radius+12),GOLD,3)

func plant(at: Vector2, grown := true) -> void:
	line(at,at-Vector2(0,35),Color("4c7b36"),5)
	line(at-Vector2(0,15),at-Vector2(15,25),Color("4c7b36"),5)
	if grown:
		for i in range(6): draw_circle(at-Vector2(0,42)+Vector2.from_angle(i*TAU/6)*10,7,GOLD)
		draw_circle(at-Vector2(0,42),5,INK)
	else:
		draw_circle(at-Vector2(0,37),9,Color("aa7256"))

func water(at: Vector2, count := 3) -> void:
	for i in range(count):
		var p := at+Vector2(i*14,0)
		line(p,p+Vector2(-4,13),Color("236e96"),4)

func container(at: Vector2, width := 90.0) -> void:
	line(at-Vector2(width/2,25),at+Vector2(-width/2+8,20))
	line(at+Vector2(-width/2+8,20),at+Vector2(width/2-8,20))
	line(at+Vector2(width/2-8,20),at+Vector2(width/2,-25))

func story(scene: String, step: int) -> void:
	draw_rect(Rect2(16,114,268,22),Color("cfddbb"))
	if scene=="garden": draw_style_box(preload("res://core/design.gd").style(Color("d9ac82")),Rect2(104,88,92,40))
	if scene=="bread": draw_circle(Vector2(150,88),48,Color("e8c794"))
	if scene=="rain": draw_rect(Rect2(24,12,252,99),Color("d6e9ec"))
	if scene=="paint": draw_rect(Rect2(88,18,124,114),Color("fff5db"))
	match scene:
		"garden":
			container(Vector2(150,110),90)
			line(Vector2(114,95),Vector2(186,95),Color("d9b181"),6)
			if step == 0: draw_circle(Vector2(150,91),8,GOLD)
			if step == 1:
				draw_rect(Rect2(90,25,40,25),INK,false,3)
				line(Vector2(130,40),Vector2(155,58),INK,6)
				water(Vector2(145,65))
			if step >= 2: plant(Vector2(150,94),step>=3)
		"bread":
			if step < 2:
				container(Vector2(150,95),130)
				for i in range(6): draw_circle(Vector2(105+i*17,84),6,Color("d9b181"))
				if step == 1:
					line(Vector2(150,85),Vector2(190,30),GOLD,7)
					draw_arc(Vector2(150,75),26,0,PI,16,INK,3)
			elif step == 2:
				draw_rect(Rect2(85,25,130,105),INK,false,4)
				draw_rect(Rect2(100,50,100,60),GOLD,false,3)
				for x in [115,145,175]: line(Vector2(x,68),Vector2(x+6,92),GOLD,3)
			else:
				draw_arc(Vector2(150,95),65,0,PI,24,INK,3)
				draw_rect(Rect2(105,58,90,40),Color("d9b181"))
				for x in [120,145,170]: line(Vector2(x,61),Vector2(x+8,78),Color("6f422e"),3)
		"rain":
			if step < 2:
				for x in [115,140,165]: draw_circle(Vector2(x,35),20,INK)
				water(Vector2(110,65),5)
			else: sun(Vector2(110,40))
			if step == 1:
				draw_arc(Vector2(170,105),45,PI,TAU,24,GOLD,8)
				line(Vector2(125,105),Vector2(215,105),GOLD,3)
				line(Vector2(170,105),Vector2(170,140),GOLD,4)
			elif step == 2:
				line(Vector2(190,65),Vector2(190,120),GOLD,5)
				draw_colored_polygon(PackedVector2Array([Vector2(190,55),Vector2(175,100),Vector2(205,100)]),GOLD)
		"kite":
			if step == 0: draw_rect(Rect2(105,30,90,90),INK,false,3)
			else:
				var p := PackedVector2Array([Vector2(150,20),Vector2(190,60),Vector2(150,100),Vector2(110,60)])
				draw_colored_polygon(p,Color("236e96"))
				line(Vector2(150,20),Vector2(150,100),INK,3)
				if step >= 2: line(Vector2(150,100),Vector2(185,140),GOLD,3)
				if step == 3:
					for y in [40,65,90]: line(Vector2(45,y),Vector2(95,y),INK,3)
		"paint":
			draw_rect(Rect2(90,20,120,110),INK,false,3)
			if step == 1:
				draw_circle(Vector2(150,75),22,GOLD)
				line(Vector2(165,70),Vector2(230,30),Color("d9b181"),8)
			if step == 2: sun(Vector2(150,75),23)
		"picnic":
			if step < 3:
				container(Vector2(150,100),110)
				if step >= 1: fruit(Vector2(150,82),18,"apple")
				if step == 2:
					line(Vector2(95,73),Vector2(205,73),INK,5)
					draw_arc(Vector2(150,73),35,PI,TAU,20,INK,4)
			elif step == 3:
				person(Vector2(130,65),26)
				container(Vector2(190,90),65)
				for x in [90,125,160]: draw_circle(Vector2(x,125),5,INK)
			else:
				draw_rect(Rect2(75,70,150,55),Color("315d85"))
				person(Vector2(85,50),20)
				person(Vector2(215,50),20)
				fruit(Vector2(150,90),20,"apple")

func flag(at: Vector2) -> void:
	line(at,at-Vector2(0,40),INK,3)
	draw_colored_polygon(PackedVector2Array([at-Vector2(0,40),at-Vector2(-25,30),at-Vector2(0,20)]),GOLD)

func draw_setting(experiment: String, control: int, value: int) -> void:
	match experiment:
		"ramp":
			if control == 0:
				line(Vector2(95,100),Vector2(205,100-value*20),INK,6)
				draw_circle(Vector2(195,88-value*20),10,GOLD)
			else:
				line(Vector2(90,85),Vector2(210,85),INK,4)
				if value == 1:
					for x in range(90,211,15): line(Vector2(x,80),Vector2(x+6,69),GOLD,3)
		"light":
			if control == 0:
				draw_rect(Rect2(100,65,55,30),INK,false,3)
				line(Vector2(155,80),Vector2(205,30+value*25),GOLD,6)
			else:
				draw_rect(Rect2(125,25,50,90),INK,false,3)
				if value == 0: draw_rect(Rect2(130,30,40,80),INK)
		"water":
			if control == 0:
				line(Vector2(110,40),Vector2(150,70),INK,5)
				line(Vector2(150,70),Vector2(95+value*55,105),INK,5)
				for x in [95,150,205]: container(Vector2(x,112),30)
				plant(Vector2(150,111),false)
			else:
				line(Vector2(100,70),Vector2(200,70),INK,7)
				line(Vector2(150,40),Vector2(150 if value == 0 else 180,100 if value == 0 else 40),GOLD,6)
		"wind":
			if control == 0:
				line(Vector2(150,105),Vector2(150,35),INK,4)
				if value > 0: draw_colored_polygon(PackedVector2Array([Vector2(150,40),Vector2(150+value*25,90),Vector2(150,90)]),GOLD)
			else:
				for i in range(value+1): line(Vector2(100,50+i*20),Vector2(200,50+i*20),INK,4)
		"balance":
			for i in range(value): draw_circle(Vector2(125+i*24,75),10,INK)
			line(Vector2(95,100),Vector2(205,100),GOLD,3)
			person(Vector2(80 if control == 0 else 220,65),15)
		"garden":
			if control == 0:
				water(Vector2(110,60),value*2)
				container(Vector2(150,105),80)
			else:
				for i in range(value): sun(Vector2(120+i*55,70),13)

func experiment_view() -> void:
	var experiment: String = spec.experiment
	var values: Array = spec.values
	var result: int = spec.result
	if spec.get("goal",false): flag(Vector2(255,65))
	match experiment:
		"ramp", "wind":
			line(Vector2(35,105),Vector2(265,105),INK,3)
			for i in range(7): line(Vector2(40+i*34,101),Vector2(40+i*34,112),INK,2)
			var x := 40.0 + result*34
			if experiment == "ramp": draw_circle(Vector2(x,90),12,GOLD)
			else:
				container(Vector2(x,90),40)
				line(Vector2(x,75),Vector2(x,35),INK,3)
				draw_colored_polygon(PackedVector2Array([Vector2(x,35),Vector2(x+25,65),Vector2(x,65)]),GOLD)
		"light", "water", "garden":
			draw_rect(Rect2(170,110,70,27),Color("ac7048"))
			plant(Vector2(205,112),result==1)
			if experiment == "light":
				draw_rect(Rect2(24,57,55,35),Color("e2ba59"))
				draw_circle(Vector2(80,74),15,Color("a66c22"))
				var destination := Vector2(205,74) if int(values[0])==2 else Vector2(150,24+int(values[0])*20)
				if int(values[1])==1:
					draw_colored_polygon(PackedVector2Array([Vector2(86,66),destination-Vector2(0,16),destination+Vector2(0,16),Vector2(86,82)]),Color("f1d57e"))
				line(Vector2(79,58),Vector2(79,90),INK,4)
			else:
				draw_style_box(preload("res://core/design.gd").style(Color("90cddd")),Rect2(25,14,55,48))
				line(Vector2(32,35),Vector2(73,35),Color("236e96"),3)
				line(Vector2(53,62),Vector2(53,83),INK,12)
				line(Vector2(53,83),Vector2(137,83),INK,12)
				var destination := 205.0
				if experiment=="water": destination=[95.0,205.0,265.0][int(values[0])]
				var flowing := int(values[1])==1 if experiment=="water" else int(values[0])>0
				line(Vector2(137,83),Vector2(destination,105),INK,12)
				if flowing:
					line(Vector2(53,62),Vector2(53,83),Color("236e96"),6)
					line(Vector2(53,83),Vector2(137,83),Color("236e96"),6)
					line(Vector2(137,83),Vector2(destination,105),Color("236e96"),6)
					water(Vector2(destination-7,109),2)
				line(Vector2(108,70),Vector2(108,94) if flowing else Vector2(132,70),Color("92541e"),5)
				if experiment=="garden":
					for i in range(int(values[1])): sun(Vector2(255+i*22,28),8)
					if int(values[0])==2: water(Vector2(160,128),5)
		"balance":
			line(Vector2(150,60),Vector2(150,125),GOLD,5)
			var tilt := 0 if result==1 else (18 if values[0]>values[1] else -18)
			line(Vector2(60,70+tilt),Vector2(240,70-tilt),INK,4)
			for side in range(2):
				var x := 75+side*150
				var y := 75+tilt*(1 if side==0 else -1)
				for i in range(int(values[side])): draw_circle(Vector2(x+(i-1)*17,y-15),7,INK)

func identity(at: Vector2, index: int) -> void:
	person(at,30)
	if index==0:
		draw_colored_polygon(PackedVector2Array([at+Vector2(-13,-31),at+Vector2(0,-40),at+Vector2(13,-31)]),INK)
	else:
		line(at+Vector2(-12,-31),at+Vector2(12,-31),INK,5)
		line(at+Vector2(-12,-37),at+Vector2(12,-37),INK,3)

func symbol(key: String, at: Vector2, outline := false) -> void:
	var color := INK if outline else GOLD
	match key:
		"apple", "pear": fruit(at,11,key,outline)
		"sun": sun(at,9)
		"shade":
			draw_arc(at+Vector2(0,8),14,PI,TAU,16,color,3)
			line(at+Vector2(0,8),at+Vector2(0,24),color,3)
		"music":
			line(at+Vector2(4,-12),at+Vector2(4,8),color,3)
			draw_circle(at+Vector2(-2,9),6,color,not outline)
		"quiet":
			draw_arc(at,12,PI/2,PI*1.5,16,color,3)
			line(at+Vector2(-15,-14),at+Vector2(15,14),color,3)
		"blocks": draw_rect(Rect2(at-Vector2(9,9),Vector2(18,18)),color,not outline, -1 if not outline else 2)
		"tool":
			line(at+Vector2(0,-15),at+Vector2(0,10),color,4)
			draw_rect(Rect2(at+Vector2(-8,5),Vector2(16,14)),color,not outline,-1 if not outline else 2)
		"water": water(at-Vector2(15,9),3)
		"space": draw_rect(Rect2(at-Vector2(14,10),Vector2(28,20)),color,false,3)
		"play":
			draw_circle(at,13,color,false,3)
			line(at-Vector2(8,8),at+Vector2(8,8),color,2)
	if outline: draw_arc(at,20,0,TAU,24,INK,1.5)

func plan(gives: Array) -> void:
	for who in range(2):
		identity(Vector2(55+who*150,45),who)
		var ordinal := 0
		for key in gives[who]:
			for _i in range(int(gives[who][key])):
				symbol(key,Vector2(35+who*150+(ordinal%3)*35,94+(ordinal/3)*30))
				ordinal += 1
		if ordinal==0: draw_arc(Vector2(70+who*150,95),18,0,TAU,24,INK,2)

func village() -> void:
	for who in range(2):
		identity(Vector2(55+who*150,43),who)
		var ordinal := 0
		for key in spec.people[who].needs:
			for i in range(int(spec.people[who].needs[key])):
				var available: int = spec.gives[who].get(key,0)
				symbol(key,Vector2(35+who*150+(ordinal%3)*35,95+(ordinal/3)*30),i>=available)
				ordinal += 1

func plan_detail(style: String) -> void:
	match style:
		"kopfhoerer":
			draw_arc(Vector2(205,30),25,PI,TAU,20,INK,3)
			line(Vector2(180,30),Vector2(180,50),INK,6)
			line(Vector2(230,30),Vector2(230,50),INK,6)
		"raeume", "bereiche": line(Vector2(150,15),Vector2(150,135),INK,3)
		"wechsel", "plan", "absprache":
			line(Vector2(115,35),Vector2(170,35),GOLD,3)
			line(Vector2(170,35),Vector2(160,25),GOLD,3)
			line(Vector2(115,50),Vector2(170,50),INK,3)
			line(Vector2(115,50),Vector2(125,60),INK,3)
		"teller": draw_arc(Vector2(150,112),100,0,PI,32,INK,3)
