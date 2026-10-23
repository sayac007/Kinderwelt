extends Control
signal station_requested(index: int)
const Art = preload("res://core/quest/art.gd")
const Scenery=preload("res://core/quest/scenery.gd")
const Props=preload("res://games/quest/world_props.gd")
const Progress = preload("res://games/quest/progress.gd")
var host: Control
var subject := "math"
var vehicle: Control
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
	clip_contents=true
	host = owner_host
	subject = area
	missions = Progress.tasks(subject)
	reduced_motion = host.store.data.reduced_motion
	hero = preload("res://core/quest/hero.gd").new()
	hero.person = host.store.data.hero
	hero.costume = host.store.data.looks[host.store.data.hero]
	hero.selected = true
	hero.reduced_motion = reduced_motion
	add_child(hero)
	vehicle=preload("res://games/quest/vehicle.gd").new()
	vehicle.size=Vector2(160,75)
	add_child(vehicle)
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
	page_label.add_theme_font_size_override("font_size",15)
	var badge:=StyleBoxFlat.new();badge.bg_color=Color("fff8e5");badge.border_color=Color("9a927e")
	badge.set_corner_radius_all(16);badge.set_border_width_all(1)
	page_label.add_theme_stylebox_override("normal",badge)
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
	page_label.position=Vector2(60,8);page_label.size=Vector2(size.x-120,48)
	page_label.text="%s %d\n%d–%d / %d" % [host.t("page"),page+1,first_station()+1,last_station()+1,missions.size()]
func station_x(index: int) -> float: return 245.0+(index-first_station())*SPACING
func tree_scale() -> float: return clampf((size.y-110)/240,.2,.8)
func camera_limit() -> float:
	return maxf(0,station_x(last_station())-100) if scene_id()=="tree" else maxf(0,station_x(last_station())+190-size.x)
func follow_camera() -> float:
	return clampf(hero_x-(100 if scene_id()=="tree" else size.x*.3),0,camera_limit())
func ground(x: float) -> float:
	return size.y*(.77 if scene_id()=="city" else .71)+sin(x/200.0)*size.y*.035
func path_point(distance: float) -> Vector2:
	if scene_id()=="tree":
		return Vector2(size.x*(.5+.17*sin(distance/SPACING*PI)),size.y-20-(distance-camera_x-100)*tree_scale())
	var y:=ground(distance)
	if scene_id()=="seabed":y=size.y*.70+sin(distance/180)*minf(36,size.y*.07)
	return Vector2(distance-camera_x,y)
func station_center(index: int) -> Vector2:
	var point:=path_point(station_x(index))
	point.y-=24 if scene_id()=="tree" else 50
	if scene_id()!="tree": point.y=clampf(point.y,96,maxf(96,size.y-48))
	return point
func motion_mode(moving: bool) -> String:
	if celebration>0:return "success"
	if not moving:return "idle"
	return {"tree":"climb","seabed":"swim","city":"drive","moon":"moon"}.get(scene_id(),"move")
func arrival_distance(index: int) -> float:
	return station_x(index)+(0 if scene_id()=="tree" else -63)
func request_station(index: int) -> void:
	if index<first_station() or index>last_station(): return
	pending = index
	target_x = arrival_distance(index)
	first_hint = false
func _process(delta: float) -> void:
	if not is_instance_valid(hero): return
	clock += delta
	if celebration<=0 and advance_target>=0:
		target_x=advance_target
		advance_target=-1
	var moving := absf(target_x-hero_x)>1
	var scene:=scene_id()
	hero.facing = -1.0 if target_x<hero_x else 1.0
	hero_x = move_toward(hero_x,target_x,(310.0 if scene=="city" else 200.0 if scene=="tree" else 230.0)*minf(delta,.05))
	celebration = maxf(0,celebration-delta)
	hero.animation=motion_mode(moving)
	manual_camera = maxf(0,manual_camera-delta)
	if manual_camera<=0: camera_x = move_toward(camera_x,follow_camera(),360.0*minf(delta,.05))
	var height := minf(250,maxf(90,size.y*.43))
	if scene in ["tree","seabed"]:height=clampf(size.y*.35,76,175)
	if scene=="city":height=clampf(size.y*.29,70,120)
	hero.size = Vector2(height*hero.aspect(),height)
	var foot:=path_point(hero_x)
	var jump:=absf(sin(clock*3.4))*minf(30,size.y*.08) if moving and scene=="moon" and not reduced_motion else 0.0
	hero.pivot_offset=hero.size/2
	hero.position = foot-Vector2(hero.size.x/2,height+(-8 if scene=="city" else -18)+jump)
	hero.rotation=0
	if moving and not reduced_motion:
		if scene=="seabed":hero.rotation=hero.facing*.32+sin(clock*2)*.04
		elif scene=="tree":hero.rotation=sin(clock*5)*.045
	vehicle.visible=scene=="city"
	vehicle.position=foot-Vector2(80,47)
	vehicle.facing=hero.facing
	if moving and not reduced_motion:vehicle.phase+=delta*8
	vehicle.queue_redraw()
	if absf(target_x-hero_x)<=1 and pending>=0:
		var station := pending
		pending = -1
		station_requested.emit(station)
	queue_redraw()
func scene_id() -> String:
	return Scenery.resolve(host.store.data,subject,page)
func marine_centers() -> Array[Vector2]:
	var result: Array[Vector2]=[]
	var phase:=0.0 if reduced_motion else clock
	for i in range(6):
		result.append(Vector2(fposmod(i*173+phase*(16+i*3),size.x+120)-60,78+fposmod(i*71+sin(phase+i)*12,maxf(36,size.y*.48))))
	return result
func ghost_centers() -> Array[Vector2]:
	var result: Array[Vector2]=[]
	var phase:=0.0 if reduced_motion else clock
	for i in range(3):
		result.append(Vector2(fposmod(size.x*(.18+i*.34)+sin(phase*.45+i)*size.x*.12,size.x+40)-20,80+sin(phase*.8+i*1.7)*24))
	return result
func draw_ghost(center: Vector2) -> void:
	var col:=Color(.94,.98,1,.76)
	draw_circle(center,15,col)
	var body:=PackedVector2Array([center+Vector2(-15,0),center+Vector2(-16,24),center+Vector2(-8,18),center+Vector2(0,25),center+Vector2(8,18),center+Vector2(16,24),center+Vector2(15,0)])
	draw_colored_polygon(body,col)
	for x in [-5,5]:draw_circle(center+Vector2(x,0),2.5,Color("38577a"))
	draw_arc(center+Vector2(0,5),4,0,PI,12,Color("38577a"),1.5,true)
func _draw() -> void:
	if host==null: return
	var scene:=scene_id()
	var tint: Color = {"math":Color(1,.98,.94),"german":Color(.90,.97,1),"logic":Color(.96,.91,1)}.get(subject,Color(.96,1,.95))
	Scenery.paint(self,scene,Rect2(Vector2.ZERO,size),tint if scene=="mountains" else Color.WHITE,clampf(hero_x/station_x(last_station()),0,1))
	var phase:=0.0 if reduced_motion else clock
	if scene=="seabed":
		var creatures:=marine_centers()
		for i in range(creatures.size()):
			Art.object(self,"fish" if i%3 else "turtle",Rect2(creatures[i],Vector2(53,38)))
		for i in range(8):
			var bubble:=Vector2(fposmod(i*119+sin(phase+i)*12,size.x),fposmod(size.y-i*57-phase*13,maxf(1,size.y)))
			draw_arc(bubble,3+i%3,0,TAU,12,Color(.7,.95,1,.55),1.5,true)
	if scene=="castle":
		for center in ghost_centers():draw_ghost(center)
	# Old walking trails remain; new worlds use branches, open water or a road.
	if scene not in ["tree","seabed"]:
		var trail := PackedVector2Array()
		for x in range(-50,int(size.x)+70,14): trail.append(Vector2(x,ground(x+camera_x)))
		draw_polyline(trail,Color("76528c") if scene=="home" else Color("a47855"),66,true)
		draw_polyline(trail,Color("79849b") if scene=="city" else Color("b4afd7") if scene=="moon" else Color("c6a2d3") if scene=="home" else Color("c5c2ca") if scene=="castle" else Color("f5d5a2"),58,true)
		if scene=="city":
			for i in range(ceil(size.x/90)+1):
				var x:=fposmod(i*90-camera_x,size.x+90)-45
				draw_line(Vector2(x,ground(x+camera_x)),Vector2(x+36,ground(x+36+camera_x)),Color("fff4c5"),3,true)
		else:draw_polyline(trail,Color("ffe5b7"),3,true)
	for n in range(first_station(),last_station()+1):
		var center := station_center(n)
		if center.x < -120 or center.x>size.x+120 or center.y< -100 or center.y>size.y+100: continue
		var solved: bool = host.store.data.quest.solved.has(missions[n].id)
		var clue: String="?" if missions[n].has("riddle_scene") else missions[n].get("object","star")
		if scene in ["tree","seabed","city","moon"]:
			match scene:
				"tree":Props.branch(self,center,phase)
				"seabed":
					if n%3==1:Props.wreck(self,center+Vector2(90,-25))
					Props.chest(self,center,solved)
				"city":Props.city_prop(self,center,n)
				"moon":Props.beacon(self,center,phase)
			# A clear task medallion keeps hidden stations discoverable without reading.
			if scene=="tree":
				if solved:Art.star(self,center+Vector2(0,7),18,Color("fff5bc"))
				elif clue=="?":Art.text(self,"?",center+Vector2(0,7),27,Color("76528c"))
				else:Art.object(self,clue,Rect2(center+Vector2(-17,-9),Vector2(34,34)))
				Art.text(self,str(n+1),center+Vector2(34,40),15,Color("fff5bc"))
			else:Props.clue(self,center,solved,clue,n)
		else:
			# Upright irregular pennants replace a menu of square buttons.
			draw_line(center+Vector2(0,30),center+Vector2(0,66),Color("785b49"),7,true)
			var shape := PackedVector2Array([center+Vector2(-37,-38),center+Vector2(32,-42),center+Vector2(41,19),center+Vector2(0,37),center+Vector2(-40,21)])
			draw_colored_polygon(shape,Color("e6ac43") if solved else Color("fff9e9"))
			draw_polyline(shape+PackedVector2Array([shape[0]]),Art.INK,2.5,true)
			if solved: Art.star(self,center,23,Color("fff5bc"))
			else:
				var task: Dictionary = missions[n]
				if clue=="?":Art.text(self,"?",center,37,Color("76528c"))
				else:Art.object(self,task.get("object","star"),Rect2(center-Vector2(27,27),Vector2(54,54)))
			Art.text(self,str(n+1),center+Vector2(0,86),16,Color("334451"))
	if first_hint:
		var c := station_center(first_station())+Vector2(-50 if scene=="tree" else 0,-52)
		if size.y<250:c=station_center(first_station())+Vector2(-55,-6)
		var hop := 0.0 if reduced_motion else sin(clock*3)*7
		draw_circle(c+Vector2(0,hop),27,Color("fff9e9"))
		Art.text(self,"☝",c+Vector2(0,hop),32)
	# Foreground flowers and grass give walking depth, without occluding targets.
	for i in range(8 if scene=="mountains" else 0):
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
			pan_camera(event.relative)
			manual_camera = 3.0
	elif event is InputEventMouseButton and event.device!=InputEvent.DEVICE_ID_EMULATION and event.button_index==MOUSE_BUTTON_LEFT:
		if event.pressed: down=event.position;pressed=true;dragging=false
		elif pressed:
			pressed=false
			if event.position.distance_to(down)<18 and not dragging: tap(event.position)
	elif event is InputEventMouseMotion and pressed:
		if event.position.distance_to(down)>18:dragging=true
		if dragging:pan_camera(event.relative)
	accept_event()
func pan_camera(relative: Vector2) -> void:
	camera_x=clampf(camera_x+(relative.y/tree_scale() if scene_id()=="tree" else -relative.x),0,camera_limit())
	manual_camera=3
	queue_redraw()
func tap(point: Vector2) -> void:
	manual_camera = 0
	for i in range(first_station(),last_station()+1):
		if point.distance_to(station_center(i))<58: request_station(i);return
	if point.y>64:
		pending = -1
		target_x = clampf((size.y-20-point.y)/tree_scale()+camera_x+100 if scene_id()=="tree" else point.x+camera_x,40,station_x(last_station())+100)
		first_hint = false
func cancel_gesture() -> void:
	pressed = false
	dragging = false
