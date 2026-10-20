extends Control
# Original procedural pictograms. Meanings use shape, grouping and outlines,
# never color alone. All labels are optional supplements to these drawings.
var spec: Dictionary = {}
var crossing := 0.0:
	set(value):
		crossing = value
		queue_redraw()
var phase := 0.0:
	set(value):
		phase = value
		queue_redraw()
const INK := Color("e5f5ff")
const GOLD := Color("ffdc78")
const WATER := Color("315d85")

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	if spec.get("kind") == "bridge":
		var total := 0
		for count in spec.get("pieces", []): total += int(count)
		if total == int(spec.get("target", 1)):
			if spec.get("reduced_motion", false): crossing = 1.0
			else:
				var walk := create_tween()
				walk.tween_property(self, "crossing", 1.0, 0.8)
	if spec.get("hint", false) and not spec.get("reduced_motion", false):
		var tween := create_tween().set_loops()
		tween.tween_property(self, "phase", 1.0, 0.5)
		tween.tween_property(self, "phase", 0.0, 0.5)

func line(a: Vector2, b: Vector2, color: Color = INK, width: float = 4.0) -> void:
	draw_line(a, b, color, width, true)

func fruit(center: Vector2, radius: float, kind: String, ghost := false) -> void:
	var color := Color("fbab84") if kind == "apple" else Color("b7df89")
	if ghost:
		draw_arc(center, radius, 0, TAU, 24, INK, 2, true)
		if kind == "pear":
			line(center+Vector2(-radius*0.7,0), center+Vector2(0,-radius*1.2), INK, 2)
			line(center+Vector2(0,-radius*1.2), center+Vector2(radius*0.7,0), INK, 2)
	elif kind == "pear":
		draw_circle(center+Vector2(0, radius*0.2), radius*0.85, color)
		draw_colored_polygon(PackedVector2Array([center+Vector2(-radius*0.7,0), center+Vector2(0,-radius*1.3), center+Vector2(radius*0.7,0)]), color)
	else:
		draw_circle(center, radius, color)
		line(center+Vector2(-radius*0.45,0), center+Vector2(radius*0.45,0), Color("6f422e"), 2)
	line(center+Vector2(0,-radius), center+Vector2(radius*0.25,-radius*1.45), INK, 2)

func person(c: Vector2, r: float) -> void:
	draw_circle(c+Vector2(0,-r*0.6), r*0.4, GOLD)
	draw_arc(c+Vector2(0,-r*0.65),r*0.23,0.2,PI-0.2,12,Color("322820"),1.5,true)
	line(c, c+Vector2(0,r*0.8), GOLD, r*0.35)
	line(c+Vector2(-r*0.5,r*0.1), c+Vector2(r*0.5,r*0.1), GOLD, 3)

func pointer(c: Vector2) -> void:
	line(c+Vector2(0,15), c, GOLD, 6)
	line(c, c+Vector2(-8,8), GOLD, 4)
	line(c, c+Vector2(8,8), GOLD, 4)
	draw_arc(c, 13+phase*4, PI, TAU, 16, GOLD, 2, true)

func _draw() -> void:
	var c := size / 2
	var small := minf(size.x, size.y)
	var r := small * 0.24
	var kind: String = spec.get("kind", "dots")
	if spec.get("selected", false): draw_style_box(selected_style(), Rect2(Vector2(4,4),size-Vector2(8,8)))
	match kind:
		"home":
			line(c+Vector2(-r,r),c+Vector2(-r,-r*0.2))
			line(c+Vector2(r,r),c+Vector2(r,-r*0.2))
			line(c+Vector2(-r*1.3,-r*0.1),c+Vector2(0,-r*1.2))
			line(c+Vector2(0,-r*1.2),c+Vector2(r*1.3,-r*0.1))
			line(c+Vector2(-r,r),c+Vector2(r,r))
		"undo", "retry", "replay":
			draw_arc(c, r, -PI*0.8, PI*0.7, 24, INK, 4, true)
			pointer(c+Vector2(-r, -r*0.6))
			if kind == "replay":
				line(c+Vector2(0,-8),c+Vector2(0,10),GOLD,3)
				draw_circle(c+Vector2(-4,10),4,GOLD)
		"hint":
			pointer(c-Vector2(0,7))
			for i in range(int(spec.get("stage", 0))+1): draw_circle(Vector2(c.x-12+i*12,size.y-12),3,GOLD)
		"next":
			line(c-Vector2(r,0),c+Vector2(r,0))
			line(c+Vector2(r,0),c+Vector2(0,-r))
			line(c+Vector2(r,0),c+Vector2(0,r))
		"levels":
			for x in [-1,1]:
				for y in [-1,1]: draw_rect(Rect2(c+Vector2(x*r*0.7,y*r*0.7)-Vector2(7,7),Vector2(14,14)),INK,false,3)
		"level":
			for i in range(int(spec.get("tier", 1))): draw_circle(Vector2(c.x+(i-(int(spec.get("tier",1))-1)/2.0)*18,c.y-12),6,GOLD)
			for i in range(int(spec.get("ordinal", 1))): draw_rect(Rect2(Vector2(c.x+(i-1)*14-4,c.y+8),Vector2(8,12)),INK)
			if spec.get("done", false): checkmark(Vector2(size.x-18,18), 8)
		"fruit": fruit(c, r, spec.get("fruit", "apple"))
		"piece":
			var count := int(spec.get("amount", 1))
			var unit := minf((size.x-24)/count, 24)
			for i in range(count):
				var p := c+Vector2((i-count/2.0)*unit,-13)
				draw_rect(Rect2(p,Vector2(unit-2,26)),Color("d9b181"))
				draw_circle(p+Vector2(unit/2,13),3,Color("322820"))
		"bridge": bridge()
		"basket": basket()
		"compare":
			fruit(c+Vector2(-r,8),r*0.3,"apple")
			for i in range(3): fruit(c+Vector2(r+(i-1)*r*0.55,8),r*0.22,"apple")
			line(c+Vector2(-r*0.2,-r*0.4),c+Vector2(r*0.25,0),GOLD)
			line(c+Vector2(-r*0.2,r*0.4),c+Vector2(r*0.25,0),GOLD)
			pointer(c+Vector2(r,-r))
		"instruction":
			var mode: String = spec.get("mode", "bridge")
			if mode == "compare":
				fruit(c+Vector2(-55,8),12,"apple")
				for i in range(3): fruit(c+Vector2(35+i*18,8),9,"apple")
				pointer(c+Vector2(55,-22))
			else:
				if mode == "bridge":
					draw_rect(Rect2(c+Vector2(-85,-10),Vector2(40,20)),Color("d9b181"))
				else: fruit(c+Vector2(-65,0),14,"pear" if mode=="sort" else "apple")
				line(c+Vector2(-30,0),c+Vector2(20,0),GOLD)
				line(c+Vector2(20,0),c+Vector2(10,-10),GOLD)
				line(c+Vector2(20,0),c+Vector2(10,10),GOLD)
				draw_rect(Rect2(c+Vector2(40,-20),Vector2(60,40)),INK,false,3)
				if mode == "share":
					person(c+Vector2(55,-27),9)
					person(c+Vector2(85,-27),9)
				elif mode == "sort": fruit(c+Vector2(70,0),11,"pear",true)
				elif mode == "match":
					for i in range(3): draw_circle(c+Vector2(55+i*15,0),4,INK)
				pointer(c+Vector2(-65,-28))
		"success":
			checkmark(c,r)
			person(c+Vector2(-r*2,0),r*0.7)
			person(c+Vector2(r*2,0),r*0.7)
	if spec.get("hint", false): pointer(Vector2(size.x-25,25+phase*5))
	if spec.get("error", false):
		line(Vector2(12,12),Vector2(30,30),GOLD,5)
		line(Vector2(30,12),Vector2(12,30),GOLD,5)

func checkmark(c: Vector2, r: float) -> void:
	line(c+Vector2(-r,0),c+Vector2(-r*0.25,r*0.6),GOLD,5)
	line(c+Vector2(-r*0.25,r*0.6),c+Vector2(r,-r*0.7),GOLD,5)

func selected_style() -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.2,0.4,0.55,0.5)
	style.border_color = GOLD
	style.set_border_width_all(3)
	style.set_corner_radius_all(10)
	return style

func bridge() -> void:
	var target := int(spec.get("target", 1))
	var unit := (size.x-92) / target
	var y := size.y*0.55
	draw_rect(Rect2(Vector2(46,y-6),Vector2(size.x-92,30)),WATER)
	for i in range(target): draw_rect(Rect2(Vector2(47+i*unit,y-15),Vector2(unit-3,23)),INK,false,2)
	var offset := 0
	for count in spec.get("pieces", []):
		draw_rect(Rect2(Vector2(47+offset*unit,y-13),Vector2(count*unit-4,19)),Color("d9b181"))
		for i in range(int(count)): draw_circle(Vector2(47+(offset+i+0.5)*unit,y-3),3,Color("322820"))
		offset += int(count)
	person(Vector2(lerpf(24.0,size.x-26,crossing) if offset==target else 24,y-8),15)
	line(Vector2(size.x-20,y-16),Vector2(size.x-20,y+18),INK,3)
	draw_colored_polygon(PackedVector2Array([Vector2(size.x-20,y-16),Vector2(size.x-7,y-11),Vector2(size.x-20,y-6)]),GOLD)

func basket() -> void:
	var target := int(spec.get("target", 1))
	var actual := int(spec.get("amount", 0))
	var columns := mini(5, target)
	var spacing := minf((size.x-40)/columns, 34)
	var start := Vector2(size.x/2-(columns-1)*spacing/2, size.y*0.5-4)
	var fruit_kind: String = spec.get("fruit", "apple")
	for i in range(target):
		var p := start+Vector2((i%columns)*spacing,(i/columns)*30)
		var items: Array = spec.get("items", [])
		var shown_kind: String = items[i] if i < items.size() else fruit_kind
		if i >= actual and spec.get("any_fruit", false):
			# A plain place accepts either shape; an apple outline would falsely
			# suggest that pears cannot be shared here.
			draw_arc(p, 10, 0, TAU, 24, INK, 2, true)
		else: fruit(p, 10, shown_kind, i>=actual)
	line(Vector2(14,36),Vector2(14,size.y-14),INK,3)
	line(Vector2(14,size.y-14),Vector2(size.x-14,size.y-14),INK,3)
	line(Vector2(size.x-14,size.y-14),Vector2(size.x-14,36),INK,3)
	if spec.get("person", false): person(Vector2(size.x/2,24),12)
	elif spec.get("sort", false): fruit(Vector2(size.x/2,24),11,fruit_kind)
