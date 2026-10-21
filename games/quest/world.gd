extends Control
signal station_requested(index: int)
const Art = preload("res://core/quest/art.gd")
const Progress = preload("res://games/quest/progress.gd")
var host: Control
var subject := "math"
var hero: Control
var hero_x := 100.0
var target_x := 100.0
var camera_x := 0.0
var pending := -1
var clock := 0.0
var down := Vector2.ZERO
var pressed := false
var travelled := false
var dragging := false
var reduced_motion := false
var first_hint := true
var manual_camera := 0.0
var missions: Array = []
var celebration := 0.0
var advance_target := -1.0
const SPACING := 280.0
const PAGE_SIZE := 10
var page := 0
var previous_page: Button
var next_page: Button
var page_label: Label
func setup(owner_host: Control,area: String) -> void:
	host = owner_host
	subject = area
	missions = Progress.tasks(subject)
	reduced_motion = host.store.data.reduced_motion
	hero = preload("res://core/quest/hero.gd").new()
	hero.person = host.store.data.hero
	hero.selected = true
	hero.reduced_motion = reduced_motion
	add_child(hero)
	previous_page = Button.new()
	previous_page.text = "‹"
	previous_page.tooltip_text = host.t("previous_page")
	previous_page.pressed.connect(func(): set_page(page-1))
	add_child(previous_page)
	next_page = Button.new()
	next_page.text = "›"
	next_page.tooltip_text = host.t("next_page")
	next_page.pressed.connect(func(): set_page(page+1))
	add_child(next_page)
	page_label = Label.new()
	page_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	page_label.mouse_filter = MOUSE_FILTER_IGNORE
	page_label.add_theme_font_size_override("font_size",17)
	add_child(page_label)
	resized.connect(arrange_pages)
	set_page(0)
	gui_input.connect(input_event)
	mouse_default_cursor_shape = CURSOR_POINTING_HAND
func first_station() -> int: return page*PAGE_SIZE
func last_station() -> int: return mini(missions.size(),first_station()+PAGE_SIZE)-1
func set_page(value: int) -> void:
	page = clampi(value,0,(missions.size()-1)/PAGE_SIZE)
	cancel_gesture()
	pending=-1;advance_target=-1;celebration=0
	hero_x=100;target_x=100;camera_x=0;manual_camera=0
	arrange_pages()
	queue_redraw()
func arrange_pages() -> void:
	if not is_instance_valid(page_label): return
	previous_page.position=Vector2(10,8);previous_page.size=Vector2(48,48)
	next_page.position=Vector2(size.x-58,8);next_page.size=Vector2(48,48)
	previous_page.disabled=page==0
	next_page.disabled=last_station()==missions.size()-1
	page_label.position=Vector2(60,14);page_label.size=Vector2(size.x-120,36)
	page_label.text="%s %d · %d–%d / %d" % [host.t("page"),page+1,first_station()+1,last_station()+1,missions.size()]
func station_x(index: int) -> float: return 245.0+(index-first_station())*SPACING
func ground(x: float) -> float: return size.y*.71+sin(x/200.0)*size.y*.035
func station_center(index: int) -> Vector2:
	var x := station_x(index)
	return Vector2(x-camera_x,ground(x)-50)
func request_station(index: int) -> void:
	if index<first_station() or index>last_station(): return
	pending = index
	target_x = station_x(index)-63
	first_hint = false
func _process(delta: float) -> void:
	if not is_instance_valid(hero): return
	clock += delta
	if celebration<=0 and advance_target>=0:
		target_x=advance_target
		advance_target=-1
	var moving := absf(target_x-hero_x)>1
	hero.facing = -1.0 if target_x<hero_x else 1.0
	hero_x = move_toward(hero_x,target_x,230.0*minf(delta,.05))
	celebration = maxf(0,celebration-delta)
	hero.animation = "success" if celebration>0 else ("move" if moving else "idle")
	var target_camera := clampf(hero_x-size.x*.3,0,maxf(0,station_x(last_station())+190-size.x))
	manual_camera = maxf(0,manual_camera-delta)
	if manual_camera<=0: camera_x = move_toward(camera_x,target_camera,300.0*minf(delta,.05))
	var height := minf(250,maxf(140,size.y*.43))
	hero.size = Vector2(height*.67,height)
	hero.position = Vector2(hero_x-camera_x-hero.size.x/2,ground(hero_x)-height+18)
	if not moving and pending>=0:
		var station := pending
		pending = -1
		station_requested.emit(station)
	queue_redraw()
func _draw() -> void:
	if host==null: return
	var bg: Texture2D = preload("res://assets/quest/landscape.png")
	var factor := maxf(size.x/bg.get_width(),size.y/bg.get_height())
	var dim := bg.get_size()*factor
	var tint: Color = {"math":Color(1,.98,.94),"german":Color(.90,.97,1),"logic":Color(.96,.91,1)}.get(subject,Color(.96,1,.95))
	draw_texture_rect(bg,Rect2(Vector2((size.x-dim.x)*.5-camera_x*.025,-(dim.y-size.y)*.35),dim+Vector2(camera_x*.025,0)),false,tint)
	# The tangible walking trail scrolls independently of the distant painted sky.
	var trail := PackedVector2Array()
	for x in range(-50,int(size.x)+70,14): trail.append(Vector2(x,ground(x+camera_x)))
	draw_polyline(trail,Color("a47855"),66,true)
	draw_polyline(trail,Color("f5d5a2"),58,true)
	draw_polyline(trail,Color("ffe5b7"),3,true)
	for n in range(first_station(),last_station()+1):
		var center := station_center(n)
		if center.x < -100 or center.x>size.x+100: continue
		var solved: bool = host.store.data.quest.solved.has(missions[n].id)
		# Upright irregular pennants replace a menu of square buttons.
		draw_line(center+Vector2(0,30),center+Vector2(0,66),Color("785b49"),7,true)
		var shape := PackedVector2Array([center+Vector2(-37,-38),center+Vector2(32,-42),center+Vector2(41,19),center+Vector2(0,37),center+Vector2(-40,21)])
		draw_colored_polygon(shape,Color("e6ac43") if solved else Color("fff9e9"))
		draw_polyline(shape+PackedVector2Array([shape[0]]),Art.INK,2.5,true)
		if solved: Art.star(self,center,23,Color("fff5bc"))
		else:
			var task: Dictionary = missions[n]
			Art.object(self,task.get("object","star"),Rect2(center-Vector2(27,27),Vector2(54,54)))
		Art.text(self,str(n+1),center+Vector2(0,86),16,Color("334451"))
	if first_hint:
		var c := station_center(first_station())+Vector2(0,-75)
		var hop := 0.0 if reduced_motion else sin(clock*3)*7
		draw_circle(c+Vector2(0,hop),27,Color("fff9e9"))
		Art.text(self,"☝",c+Vector2(0,hop),32)
	# Foreground flowers and grass give walking depth, without occluding targets.
	for i in range(8):
		var x := fposmod(i*197-camera_x*.8,size.x+100)-50
		Art.object(self,"flower",Rect2(Vector2(x,size.y-56),Vector2(45,55)))
func input_event(event: InputEvent) -> void:
	if event is InputEventScreenTouch and event.index==0:
		if event.pressed: down=event.position;pressed=true;dragging=false
		elif pressed:
			pressed=false
			if event.position.distance_to(down)<18 and not dragging: tap(event.position)
	elif event is InputEventScreenDrag and event.index==0 and pressed:
		if event.position.distance_to(down)>18: dragging=true
		if dragging:
			camera_x = clampf(camera_x-event.relative.x,0,maxf(0,station_x(last_station())+190-size.x))
			manual_camera = 3.0
	elif event is InputEventMouseButton and event.device!=InputEvent.DEVICE_ID_EMULATION and event.button_index==MOUSE_BUTTON_LEFT:
		if event.pressed: down=event.position;pressed=true;dragging=false
		elif pressed:
			pressed=false
			if event.position.distance_to(down)<18: tap(event.position)
	accept_event()
func tap(point: Vector2) -> void:
	manual_camera = 0
	for i in range(first_station(),last_station()+1):
		if point.distance_to(station_center(i))<58: request_station(i);return
	if point.y>size.y*.4:
		pending = -1
		target_x = clampf(point.x+camera_x,40,station_x(last_station())+100)
		first_hint = false
func cancel_gesture() -> void:
	pressed = false
	dragging = false
