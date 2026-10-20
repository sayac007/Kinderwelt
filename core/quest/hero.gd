extends Control
# Each sprite is split at the hips: legs swing around their hip independently.
# The upper body, head and backpack remain readable during walking/celebration.
const NAMES := {"mina":"Mina","leo":"Leo","sam":"Sam","jule":"Jule"}
const IDS := ["mina","leo","sam","jule"]
const SPRITES = {"mina":preload("res://assets/quest/mina.png"),"leo":preload("res://assets/quest/leo.png"),"sam":preload("res://assets/quest/sam.png"),"jule":preload("res://assets/quest/jule.png")}
var person := "mina"
var animation := "idle"
var clock := 0.0
var reduced_motion := false
var facing := 1.0
var selected := false
var reaction := 0.0
func react() -> void:
	reaction = 1.2
	animation = "success"
func _ready() -> void:
	mouse_filter = MOUSE_FILTER_IGNORE
func _process(delta: float) -> void:
	if not reduced_motion: clock += delta
	if reaction>0:
		reaction = maxf(0,reaction-delta)
		if reaction==0: animation="idle"
	queue_redraw()
func _draw() -> void:
	var texture: Texture2D = SPRITES.get(person,SPRITES.mina)
	var col := maxi(IDS.find(person),0)
	var w := float(texture.get_width())
	var h := float(texture.get_height())
	var scale_size := Vector2(size.x,size.y)
	var hue: float = [.02,.51,.12,.77][col]
	if reaction>0 and not reduced_motion: hue+=reaction*.16
	var glow := Color.from_hsv(fposmod(hue+(.08*sin(clock*1.7) if selected and not reduced_motion else 0),1),.68,1)
	var intensity := .8 if selected else .24
	if reaction>0: intensity=1.0
	draw_set_transform(Vector2(size.x*.5,size.y*.51),0,Vector2(.62,1.2))
	for i in range(16,0,-1):
		draw_circle(Vector2.ZERO,size.y*(.20+i*.006),Color(glow,intensity*.013))
	draw_set_transform(Vector2.ZERO)
	if reaction>0 and not reduced_motion:
		for j in range(5):
			var angle := j*TAU/5+clock
			var center := Vector2(size.x*.5,size.y*.45)+Vector2(cos(angle)*size.x*.6,sin(angle)*size.y*.4)
			preload("res://core/quest/art.gd").star(self,center,5+reaction*2,Color(glow,.85))
		for direction in [-1,1]:
			var origin := Vector2(size.x*.5+direction*size.x*.46,size.y*.23)
			var bolt := PackedVector2Array([origin,origin+Vector2(-direction*9,15),origin+Vector2(direction*5,13),origin+Vector2(-direction*6,29)])
			draw_polyline(bolt,Color(glow,.85),3,true)
	var bob := sin(clock*2.5)*1.5
	if animation=="move": bob = -absf(sin(clock*9))*4
	if animation=="success": bob = -absf(sin(clock*5))*14
	if reduced_motion: bob = 0
	var lean := -.08 if animation=="think" else sin(clock*4)*.025
	if reduced_motion: lean = 0
	var base := Vector2(size.x/2,size.y*.72+bob)
	var tint := Color.WHITE.lerp(glow,minf(.18,reaction*.12)) if not reduced_motion else Color.WHITE
	draw_set_transform(base,lean,Vector2(facing,1))
	var swing := sin(clock*9)*.22 if animation=="move" and not reduced_motion else 0.0
	for leg in range(2):
		var hip := Vector2((-1 if leg==0 else 1)*scale_size.x*.13,0)
		draw_set_transform(base+Vector2(hip.x*facing,0),lean+swing*(1 if leg==0 else -1),Vector2(facing,1))
		var destination := Rect2(Vector2(-scale_size.x*.5-hip.x if leg==0 else -hip.x,0),Vector2(scale_size.x*.5,scale_size.y*.28))
		draw_texture_rect_region(texture,destination,Rect2(Vector2(leg*w*.5,h*.72),Vector2(w*.5,h*.28)),tint)
	draw_set_transform(base,lean,Vector2(facing,1))
	draw_texture_rect_region(texture,Rect2(Vector2(-scale_size.x*.5,-scale_size.y*.72),Vector2(scale_size.x,scale_size.y*.72)),Rect2(Vector2.ZERO,Vector2(w,h*.72)),tint)
	draw_set_transform(Vector2.ZERO)
