extends Control
signal gesture_done(action: Dictionary)
const Gesture = preload("res://games/water/gesture.gd")
const Hero = preload("res://core/modern/hero.tscn")
var model: RefCounted
var gesture := Gesture.new()
var selected := -1
var hero: Control
var reduced_motion := false
var clock := 0.0
var growth := 0.0
var cell := 64.0
var origin := Vector2.ZERO
var phase := "idle"
var entered := 0.0
var celebration := 0.0
var was_complete := false
var watered := false
const INK := Color("354b53")
func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	clip_contents = true
	hero = Hero.instantiate()
	add_child(hero)
	gui_input.connect(input_event)
func geometry() -> void:
	if model==null: return
	var top := 82.0 if size.y>300 else 44.0
	cell = minf(92,minf((size.x-16)/model.cols,(size.y-top-4)/model.rows))
	origin = Vector2((size.x-cell*model.cols)/2,top)
func tile_at(point: Vector2) -> int:
	geometry()
	var at := Vector2i(floor((point.x-origin.x)/cell),floor((point.y-origin.y)/cell))
	return at.y*model.cols+at.x if at.x>=0 and at.x<model.cols and at.y>=0 and at.y<model.rows else -1
func input_event(event: InputEvent) -> void:
	if model==null: return
	if event is InputEventScreenTouch:
		if event.index!=0: return
		if event.pressed: gesture.begin(tile_at(event.position),event.position)
		else: gesture_done.emit(gesture.finish(tile_at(event.position)))
		accept_event()
	elif event is InputEventScreenDrag:
		if event.index==0: gesture.move(event.position); accept_event()
	elif event is InputEventMouseButton and event.button_index==MOUSE_BUTTON_LEFT:
		# On mobile the real touch above owns the transaction; emulated mouse is redundant.
		if event.device==InputEvent.DEVICE_ID_EMULATION: return
		if event.pressed: gesture.begin(tile_at(event.position),event.position)
		else: gesture_done.emit(gesture.finish(tile_at(event.position)))
		accept_event()
	elif event is InputEventMouseMotion and event.button_mask&MOUSE_BUTTON_MASK_LEFT:
		gesture.move(event.position)
func _notification(what: int) -> void:
	if what==NOTIFICATION_APPLICATION_PAUSED: gesture.cancel()
func _process(delta: float) -> void:
	if model==null: return
	geometry()
	if not reduced_motion: clock += delta
	var complete: bool = watered or model.evaluate().complete
	watered = complete
	if complete and not was_complete: celebration = 1.0
	was_complete = complete
	celebration = maxf(0,celebration-delta)
	entered = 1.0 if reduced_motion else minf(1,entered+delta/0.8)
	growth = (1.0 if complete else 0.0) if reduced_motion else move_toward(growth,1.0 if complete else 0.0,delta*1.7)
	if is_instance_valid(hero):
		hero.position = Vector2(lerpf(-60,8,entered),0)
		hero.size = Vector2(60,78 if size.y>300 else 52)
		hero.animation = "success" if celebration>0 else phase
		hero.reduced_motion = reduced_motion
	queue_redraw()
func center(index: int) -> Vector2:
	return origin+Vector2(index%model.cols+.5,index/model.cols+.5)*cell
func stroke(a: Vector2,b: Vector2,color: Color,width: float) -> void:
	draw_line(a,b,INK,width+4,true)
	draw_line(a,b,color,width,true)
	draw_circle(a,width/2,color)
	draw_circle(b,width/2,color)
func pot(at: Vector2,healthy: bool,amount: int) -> void:
	var k := cell/70
	var grow := growth if healthy else 0.0
	var rim := at+Vector2(0,10)*k
	var p := PackedVector2Array([rim+Vector2(-20,0)*k,rim+Vector2(20,0)*k,rim+Vector2(14,24)*k,rim+Vector2(-14,24)*k])
	draw_colored_polygon(p,Color("c27b55"))
	draw_polyline(p+PackedVector2Array([p[0]]),INK,2,true)
	var tip := at+Vector2(5*(1-grow),-11-18*grow)*k
	stroke(rim,tip,Color("628453"),4*k)
	for i in [-1,1]:
		var points := PackedVector2Array([tip+Vector2(0,8)*k,tip+Vector2(i*22,7-12*grow)*k,tip+Vector2(i*18,19-8*grow)*k,tip+Vector2(0,16)*k])
		draw_colored_polygon(points,Color("88a962"))
		draw_polyline(points,INK,1.8,true)
	if grow>.5:
		for i in range(5): draw_circle(tip+Vector2.from_angle(i*TAU/5)*9*k,6*k,Color("e0a44d"))
		draw_circle(tip,5*k,Color("92644a"))
	for i in range(amount): draw_circle(at+Vector2(-12+i*12,32)*k,3*k,Color("416f8b"))
func _draw() -> void:
	if model==null or size.x<1 or size.y<1: return
	geometry()
	draw_rect(Rect2(Vector2.ZERO,size),Color("e6edcf"))
	# Illustrated garden edge, irregular foliage and soil instead of boxed cells.
	for i in range(9):
		var at := Vector2(i*size.x/8,38+sin(i*2.7)*10)
		draw_circle(at,25,Color("c3d5b0"))
	draw_rect(Rect2(0,origin.y-8,size.x,size.y-origin.y+8),Color("f0e0bd"))
	for i in range(25):
		var at := Vector2(fmod(i*83.0,size.x),origin.y+fmod(i*61.0,maxf(1,size.y-origin.y)))
		draw_line(at,at+Vector2(4,1),Color("d5c49d"),1.5,true)
	var r: Dictionary = model.evaluate()
	for index in range(model.tiles.size()):
		var at := center(index)
		var ports: int = model.tiles[index]
		if index==4:
			stroke(at+Vector2(-cell*.25,cell*.25),at+Vector2(-cell*.25,-cell*.18),Color("88a4a3"),cell*.18)
			stroke(at+Vector2(-cell*.25,-cell*.18),at+Vector2(cell*.20,-cell*.18),Color("88a4a3"),cell*.18)
			stroke(at+Vector2(cell*.20,-cell*.18),at+Vector2(cell*.20,0),Color("88a4a3"),cell*.16)
			stroke(at+Vector2(cell*.2,0),at+Vector2(cell*.5,0),Color("75afbf") if model.valve else Color("9aacaa"),cell*.13)
			draw_circle(at+Vector2(-cell*.25,-cell*.31),cell*.14,Color("c67758"))
			continue
		if model.goals.has(index):
			for d in range(4):
				if ports & (1<<d): stroke(at+Vector2(model.DIRS[d])*cell*.5,at+Vector2(0,cell*.15),Color("6ca2ad") if r.supplied.has(index) else Color("99aaa0"),cell*.10)
			if model.tier==1 and index==14:
				stroke(at+Vector2(-cell*.3,.15*cell),at+Vector2(cell*.3,.15*cell),Color("5299b4") if r.supplied.has(index) else Color("81a8a8"),cell*.14)
				draw_circle(at+Vector2(0,-cell*.12),cell*.15,Color("ab7651"))
				draw_circle(at+Vector2(cell*.13,-cell*.21),cell*.10,Color("ab7651"))
				draw_circle(at+Vector2(cell*.16,-cell*.23),1.5,INK)
			else: pot(at,watered or r.supplied.has(index),model.goals[index])
			continue
		if ports==0:
			draw_circle(at,3,Color("bba582"))
			continue
		for d in range(4):
			if ports & (1<<d):
				var end := at+Vector2(model.DIRS[d])*cell*.5
				stroke(at,end,Color("b77e57"),cell*.23)
				if r.visited.has(index):
					draw_line(at,end,Color("509ab5"),cell*.10,true)
					if not reduced_motion:
						draw_circle(at.lerp(end,fmod(clock*1.5+d*.21,1)),cell*.035,Color("e9f4e8"))
		if index==selected: draw_arc(at,cell*.42,0,TAU,40,Color("376c7a"),4,true)
	for leak in r.leaks:
		var at := center(leak.cell)+Vector2(model.DIRS[leak.direction])*cell*.47
		draw_circle(at+Vector2(0,5+sin(clock*5)*3),cell*.07,Color("579ab5"))
	if gesture.dragging and gesture.start>=0:
		draw_arc(gesture.current,cell*.35,0,TAU,36,Color("366b7c"),4,true)
