extends Control
signal destination(action: String)
const Controller = preload("res://games/adventure/movement.gd")
var controller := Controller.new()
var room := 0
var powered := false
var safe := true
var source_state := {"sun":false,"wind":false,"battery":false}
var circuit_state := {"relay":false,"door":false,"lamp":false}
var opening := 0.0
var unlocked := false
var reduced_motion := false
var paused := false
var pending := ""
var clock := 0.0
var camera := 0.0
var camera_y := 0.0
var zoom := 1.0
var objects: Array = []
const INK := Color("263c4d")
func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	gui_input.connect(point_input)
	update_objects()
func update_objects() -> void:
	objects = [{"x":65.0,"id":"left","label":"← Raum"},{"x":835.0,"id":"right","label":"Raum →"}]
	if room==0:
		objects += [{"x":220.0,"id":"robot","label":"Pico"},{"x":500.0,"id":"sources","label":"Quellen"},{"x":700.0,"id":"guide","label":"Plan"}]
	elif room==1:
		objects += [{"x":230.0,"id":"sources","label":"Quellen"},{"x":460.0,"id":"circuits","label":"Pult"},{"x":680.0,"id":"guide","label":"Anzeigen"}]
	else: objects += [{"x":430.0,"id":"reward","label":"Teleskop"}]
func move_to(action: String) -> void:
	for obj in objects:
		if obj.id==action:
			pending = action
			controller.set_target(Vector2(obj.x,365))
			return
func point_input(event: InputEvent) -> void:
	var point := Vector2.ZERO
	var tapped := false
	if event is InputEventScreenTouch and event.pressed:
		point = event.position
		tapped = true
	elif event is InputEventMouseButton and event.pressed and event.button_index==MOUSE_BUTTON_LEFT:
		point = event.position
		tapped = true
	if not tapped or paused: return
	var local := Vector2(point.x/zoom+camera,point.y/zoom+camera_y)
	for obj in objects:
		if absf(local.x-obj.x)<maxf(48,38/zoom) and local.y<390:
			move_to(obj.id)
			accept_event()
			return
	pending = ""
	controller.set_target(local)
	accept_event()
func _process(delta: float) -> void:
	if not paused:
		var axis := Input.get_vector("ui_left","ui_right","ui_up","ui_down")
		if axis!=Vector2.ZERO: pending = ""
		controller.step(delta,axis)
		if controller.arrived() and not pending.is_empty():
			var action := pending
			pending = ""
			destination.emit(action)
		if not reduced_motion: clock += delta
	opening = (1.0 if unlocked else 0.0) if reduced_motion else move_toward(opening,1.0 if unlocked else 0.0,delta*2.0)
	zoom = clampf(maxf(size.y/560.0,size.x/900.0),0.12,1.2)
	var visible_width := size.x/zoom
	camera = clampf(controller.position.x-visible_width*0.5,0,maxf(0,900-visible_width))
	camera_y = clampf(controller.position.y-size.y/zoom*0.80,0,maxf(0,560-size.y/zoom))
	queue_redraw()
func words(at: Vector2,text: String,color := INK,fs := 23) -> void:
	draw_string(get_theme_default_font(),at,text,HORIZONTAL_ALIGNMENT_LEFT,-1,maxi(fs,ceili(18/zoom)),color)
func box(rect: Rect2,color: Color,radius := 16.0) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = color
	style.set_corner_radius_all(int(radius))
	draw_style_box(style,rect)
func cog(center: Vector2,r: float,color: Color) -> void:
	for i in range(8):
		var angle := i*TAU/8+(clock*0.6 if source_state.values().has(true) and safe else 0.0)
		draw_line(center+Vector2.from_angle(angle)*r*.7,center+Vector2.from_angle(angle)*r*1.12,color,12)
	draw_circle(center,r*.82,color)
	draw_circle(center,r*.35,Color("e7f3eb"))
func robot(at: Vector2) -> void:
	box(Rect2(at+Vector2(-28,-82),Vector2(56,58)),Color("55c1bb"))
	box(Rect2(at+Vector2(-36,-139),Vector2(72,59)),Color("efbd52"))
	draw_circle(at+Vector2(-14,-114),6,INK)
	draw_circle(at+Vector2(14,-114),6,INK)
	draw_arc(at+Vector2(0,-109),15,0.2,PI-.2,18,INK,3)
	draw_line(at+Vector2(0,-139),at+Vector2(0,-154),INK,4)
	draw_circle(at+Vector2(0,-158),7,Color("e27673"))
	for x in [-18,18]: draw_circle(at+Vector2(x,-12),13,INK)
func person(at: Vector2) -> void:
	var bob := sin(clock*12)*3 if not controller.arrived() else 0.0
	at.y += bob
	draw_circle(at+Vector2(0,0),25,Color(0.12,0.22,0.25,0.15))
	box(Rect2(at+Vector2(-22,-61),Vector2(44,43)),Color("e97d5b"),10)
	for x in [-12,12]:
		draw_line(at+Vector2(x,-21),at+Vector2(x,-1),INK,10)
		draw_line(at+Vector2(x*2,-49),at+Vector2(x*2,-27),Color("e7b891"),8)
	draw_circle(at+Vector2(0,-83),26,Color("e7b891"))
	draw_arc(at+Vector2(0,-88),23,PI,TAU,20,Color("674636"),12)
	for x in [-8,8]: draw_circle(at+Vector2(x,-85),3,INK)
	draw_arc(at+Vector2(0,-80),10,0.15,PI-.15,12,INK,2)
func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO,size),Color("d9eee8"))
	draw_set_transform(Vector2(-camera*zoom,-camera_y*zoom),0,Vector2(zoom,zoom))
	box(Rect2(0,0,900,320),Color("eaf3df") if room!=2 else Color("c7d5ef"))
	for x in range(100,850,180):
		box(Rect2(x,38,110,125),Color("83b9d0"))
		draw_line(Vector2(x+55,38),Vector2(x+55,163),Color("fafff3"),7)
		draw_line(Vector2(x,105),Vector2(x+110,105),Color("fafff3"),7)
	draw_rect(Rect2(0,320,900,240),Color("c9af88"))
	for y in range(338,560,44): draw_line(Vector2(0,y),Vector2(900,y),Color("b69c78"),2)
	if room==0:
		# Workbench, hanging wrench and screwdriver, all original drawn artwork.
		box(Rect2(300,264,130,22),Color("b47952"),5)
		for x in [312,411]: draw_line(Vector2(x,284),Vector2(x,326),INK,9)
		draw_line(Vector2(335,177),Vector2(335,219),INK,9)
		draw_arc(Vector2(335,172),14,.2,PI-.2,20,INK,7)
		draw_line(Vector2(384,177),Vector2(384,222),INK,5)
		box(Rect2(376,161,16,28),Color("e47c55"),4)
	for obj in objects:
		var x: float = obj.x
		if obj.id in ["left","right"]:
			var closed: bool = obj.id=="right" and room==1 and not unlocked
			box(Rect2(x-38,178,76,147),Color("46546d"))
			var fraction := opening if room==1 and obj.id=="right" else (0.0 if closed else 1.0)
			box(Rect2(x-30,188,60,137),Color("99ceac"))
			if fraction<1: box(Rect2(x-30,188,60,137*(1-fraction)),Color("db925b"))
			if closed:
				for y in range(205,310,25): draw_line(Vector2(x-28,y),Vector2(x+28,y),INK,5)
			else: words(Vector2(x-16,280),"←" if obj.id=="left" else "→")
		elif obj.id=="robot": robot(Vector2(x,310))
		elif obj.id=="sources":
			box(Rect2(x-65,208,130,112),Color("669b98"))
			cog(Vector2(x,259),32,Color("f6d570") if safe else Color("e47c55"))
			for i in range(3):
				var on: bool = source_state[["sun","wind","battery"][i]]
				draw_circle(Vector2(x-42+i*42,308),8,Color("ffe576") if on else Color("f4f0d8"))
			draw_line(Vector2(x-60,317),Vector2(x+60,317),INK,8)
		elif obj.id=="circuits":
			box(Rect2(x-66,195,132,130),Color("5d7891"))
			for i in range(3):
				draw_circle(Vector2(x-38+i*38,225),11,Color("ffda69") if circuit_state[["relay","door","lamp"][i]] and powered else Color("f4f0d8"))
				draw_line(Vector2(x-38+i*38,255),Vector2(x-38+i*38,290),Color("eff9ef"),6)
		elif obj.id=="reward":
			draw_line(Vector2(x,255),Vector2(x-45,330),INK,10)
			draw_line(Vector2(x,255),Vector2(x+45,330),INK,10)
			draw_line(Vector2(x-50,235),Vector2(x+55,183),Color("d08755"),34)
			draw_circle(Vector2(x+55,183),24,Color("5489a6"))
			for i in range(7):
				var p := Vector2(190+i*84,53+sin(i*3.0)*30)
				draw_circle(p,4+sin(clock+i)*1.5,Color("fff4b0"))
		else:
			box(Rect2(x-54,203,108,106),Color("f9f3d9"))
			for i in range(3): draw_line(Vector2(x-35,226+i*26),Vector2(x+32,226+i*26),Color("557d8d"),5)
		if obj.id not in ["left","right"]:
			var fs := maxi(23,ceili(18/zoom))
			var width := get_theme_default_font().get_string_size(obj.label,HORIZONTAL_ALIGNMENT_LEFT,-1,fs).x
			words(Vector2(x-width/2,maxf(160,camera_y+22/zoom)),obj.label)
		# Broad, visibly marked interaction footprints; tapping walks there first.
		draw_arc(Vector2(x,370),28,0,TAU,28,Color("527664"),3)
		words(Vector2(x-8,379),"•")
	if room==1:
		draw_line(Vector2(230,335),Vector2(680,335),Color("f7d465") if powered else INK,6)
		if powered:
			for i in range(8): draw_circle(Vector2(230+fmod(clock*80+i*56,450),335),4,Color.WHITE)
	if not controller.arrived():
		draw_arc(controller.target,19,0,TAU,24,Color("285c46"),4)
	person(controller.position)
	draw_set_transform(Vector2.ZERO)
