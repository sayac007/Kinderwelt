extends Control
signal changed
const Avatar=preload("res://core/quest/custom_avatar.gd")
var texture: Texture2D
var source: Image
var editable := false
var portrait := false
var zoom := 1.0
var center := Vector2(.5,.5)
var circle: TextureRect
var figure_texture: ImageTexture
var dragging := false
var touches := {}
func _ready() -> void:
	mouse_filter=MOUSE_FILTER_STOP if editable else MOUSE_FILTER_IGNORE
	clip_contents=true
	circle=TextureRect.new();circle.mouse_filter=MOUSE_FILTER_IGNORE
	circle.expand_mode=TextureRect.EXPAND_IGNORE_SIZE
	circle.stretch_mode=TextureRect.STRETCH_SCALE
	circle.material=ShaderMaterial.new();circle.material.shader=preload("res://core/quest/avatar_circle.gdshader")
	add_child(circle);circle.hide()
	resized.connect(func():cancel_gesture();refresh())
func set_source(image: Image,framed: bool) -> void:
	if not editable:return
	source=image;texture=ImageTexture.create_from_image(image)
	figure_texture=ImageTexture.create_from_image(Avatar.figure(image))
	portrait=framed;reset_crop()
func set_portrait(value: bool) -> void:
	if not editable or source==null:return
	if not value and source.detect_alpha()==Image.ALPHA_NONE:return
	portrait=value;cancel_gesture();refresh();changed.emit()
func reset_crop() -> void:
	if not editable:return
	zoom=1;center=Vector2(.5,.5);cancel_gesture();refresh();changed.emit()
func set_zoom(value: float) -> void:
	if not editable or source==null or not portrait or not is_finite(value):return
	zoom=clampf(value,1,4);clamp_center();refresh();changed.emit()
func clamp_center() -> void:
	var half:=float(mini(source.get_width(),source.get_height()))/(2*zoom)
	center.x=clampf(center.x,half/source.get_width(),1-half/source.get_width())
	center.y=clampf(center.y,half/source.get_height(),1-half/source.get_height())
func frame_rect() -> Rect2:
	var side:=maxf(1,minf(size.x,size.y)-16)
	return Rect2((size-Vector2.ONE*side)/2,Vector2.ONE*side)
func pan(delta: Vector2) -> void:
	if not editable or source==null or not portrait or not delta.is_finite():return
	var side:=float(mini(source.get_width(),source.get_height()))/zoom
	center-=delta*side/frame_rect().size.x/Vector2(source.get_size())
	clamp_center();refresh();changed.emit()
func output() -> Image:
	if source==null:return null
	return Avatar.portrait(source,center,zoom) if portrait else Avatar.figure(source)
func refresh() -> void:
	if is_instance_valid(circle):
		circle.visible=source!=null and portrait
		if circle.visible:
			var rect:=frame_rect();circle.position=rect.position;circle.size=rect.size;circle.texture=texture
			var crop:=Avatar.crop_rect(source,center,zoom)
			circle.material.set_shader_parameter("region",Vector4(float(crop.position.x)/source.get_width(),float(crop.position.y)/source.get_height(),float(crop.size.x)/source.get_width(),float(crop.size.y)/source.get_height()))
	queue_redraw()
func cancel_gesture() -> void:
	dragging=false;touches.clear()
func _notification(what: int) -> void:
	if what in [NOTIFICATION_WM_WINDOW_FOCUS_OUT,NOTIFICATION_APPLICATION_PAUSED]:cancel_gesture()
func _gui_input(event: InputEvent) -> void:
	if not editable or source==null or not portrait:return
	if event is InputEventScreenTouch:
		if event.pressed:touches[event.index]=event.position
		else:touches.erase(event.index)
		accept_event()
	elif event is InputEventScreenDrag and touches.has(event.index):
		var before: Array=touches.values()
		var previous: Vector2=touches[event.index]
		touches[event.index]=event.position
		if touches.size()==2:
			var after: Array=touches.values()
			var distance: float=before[0].distance_to(before[1])
			if distance>4:set_zoom(zoom*after[0].distance_to(after[1])/distance)
		else:pan(event.position-previous)
		accept_event()
	elif event is InputEventMagnifyGesture:
		set_zoom(zoom*event.factor);accept_event()
	elif event is InputEventMouseButton and event.device!=InputEvent.DEVICE_ID_EMULATION and touches.is_empty():
		if event.button_index==MOUSE_BUTTON_LEFT:dragging=event.pressed
		elif event.pressed and event.button_index==MOUSE_BUTTON_WHEEL_UP:set_zoom(zoom*1.1)
		elif event.pressed and event.button_index==MOUSE_BUTTON_WHEEL_DOWN:set_zoom(zoom/1.1)
		accept_event()
	elif event is InputEventMouseMotion and dragging and touches.is_empty() and event.device!=InputEvent.DEVICE_ID_EMULATION:
		pan(event.relative);accept_event()
func _draw() -> void:
	# Two mattes make leftover white rectangles visible without erasing white fur.
	for y in range(ceili(size.y/24.0)):
		for x in range(ceili(size.x/24.0)):
			var dark := x*24>=size.x/2
			var color := Color("304657") if dark else Color("f2eee5")
			if (x+y)%2==0: color=color.lightened(.12) if dark else color.darkened(.08)
			draw_rect(Rect2(x*24,y*24,minf(24,size.x-x*24),minf(24,size.y-y*24)),color)
	if source!=null and portrait:
		var rect:=frame_rect()
		draw_arc(rect.get_center(),rect.size.x/2+2,0,TAU,96,Color("ffd168"),3,true)
	elif texture!=null:
		var shown: Texture2D=figure_texture if figure_texture!=null else texture
		var fitted := shown.get_size()*minf((size.x-24)/shown.get_width(),(size.y-24)/shown.get_height())
		draw_texture_rect(shown,Rect2((size-fitted)/2,fitted),false)
