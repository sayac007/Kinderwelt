extends Control
# Original articulated 2D children; shared body parts, no raster atlases or textures.
const PEOPLE := {
 "mina":{"name":"Mina","skin":"bd835f","hair":"382d36","shirt":"da7455","pants":"304d6d","style":0},
 "leo":{"name":"Leo","skin":"e7b78a","hair":"875b36","shirt":"488f91","pants":"344461","style":1},
 "sam":{"name":"Sam","skin":"885841","hair":"292d3a","shirt":"d4a539","pants":"314e62","style":2},
 "jule":{"name":"Jule","skin":"f2cfac","hair":"ae6645","shirt":"8976af","pants":"385f63","style":3}}
var person := "mina"
var animation := "idle"
var reduced_motion := false
var clock := 0.0
const INK := Color("293b4b")
func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
func _process(delta: float) -> void:
	if not reduced_motion: clock += delta
	queue_redraw()
func line(a: Vector2,b: Vector2,color: Color,width: float) -> void:
	draw_line(a,b,INK,width+3,true)
	draw_line(a,b,color,width,true)
	draw_circle(b,width/2,color)
func oval(at: Vector2,radius: float,color: Color) -> void:
	draw_circle(at,radius+1.5,INK)
	draw_circle(at,radius,color)
func _draw() -> void:
	var p: Dictionary = PEOPLE.get(person,PEOPLE.mina)
	var skin := Color(p.skin)
	var shirt := Color(p.shirt)
	var pants := Color(p.pants)
	var hair := Color(p.hair)
	var scale_factor := minf(size.x/112,size.y/170)
	var bob := sin(clock*2)*1.3
	if animation=="move": bob = absf(sin(clock*9))*3
	elif animation=="success": bob = -absf(sin(clock*5))*8
	if reduced_motion: bob = 0
	draw_set_transform(Vector2(size.x/2,size.y*.94+bob*scale_factor),0,Vector2(scale_factor,scale_factor))
	shadow_ellipse(Vector2(0,0),Vector2(36,5),Color(0.15,0.23,0.26,.12))
	var swing := sin(clock*8)*12 if animation=="move" and not reduced_motion else 0.0
	line(Vector2(-11,-50),Vector2(-13+swing,-8),pants,13)
	line(Vector2(11,-50),Vector2(14-swing,-8),pants,13)
	line(Vector2(-18+swing,-4),Vector2(-6+swing,-4),Color("f3eee0"),10)
	line(Vector2(9-swing,-4),Vector2(23-swing,-4),Color("f3eee0"),10)
	var torso := PackedVector2Array([Vector2(-22,-99),Vector2(20,-99),Vector2(24,-49),Vector2(-25,-49)])
	draw_colored_polygon(torso,shirt)
	draw_polyline(torso+PackedVector2Array([torso[0]]),INK,2.5,true)
	line(Vector2(0,-109),Vector2(0,-99),skin,12)
	var left := Vector2(-33,-64+swing*.4)
	var right := Vector2(31,-66-swing*.4)
	if animation=="think": right = Vector2(14,-108)
	elif animation=="success":
		left = Vector2(-41,-126)
		right = Vector2(42,-127)
	elif p.style==1: left = Vector2(-29,-54)
	line(Vector2(-21,-91),left,skin,9)
	line(Vector2(21,-91),right,skin,9)
	line(Vector2(-21,-91),Vector2(-26,-80),shirt,13)
	line(Vector2(21,-91),Vector2(25,-80),shirt,13)
	# Human proportions and small eyes, asymmetrical hair and clothing details.
	oval(Vector2(0,-128),23,skin)
	if p.style==0:
		draw_arc(Vector2(0,-132),23,PI,TAU,20,hair,12,true)
		oval(Vector2(-26,-134),11,hair)
		oval(Vector2(26,-132),12,hair)
	elif p.style==1:
		draw_colored_polygon(PackedVector2Array([Vector2(-23,-135),Vector2(-18,-156),Vector2(4,-161),Vector2(24,-145),Vector2(17,-137),Vector2(2,-147)]),hair)
	elif p.style==2:
		for i in range(6): oval(Vector2(-21+i*8,-147+sin(i*1.7)*3),8,hair)
	else:
		draw_arc(Vector2(0,-132),24,PI,TAU,20,hair,12,true)
		line(Vector2(-23,-129),Vector2(-25,-105),hair,10)
		line(Vector2(22,-130),Vector2(25,-108),hair,10)
	for x in [-8,8]: draw_circle(Vector2(x,-128),2.2,INK)
	if p.style==3:
		for x in [-8,8]: draw_arc(Vector2(x,-128),7,0,TAU,24,INK,1.8,true)
		draw_line(Vector2(-1,-128),Vector2(1,-128),INK,2)
	draw_line(Vector2(-18,-134),Vector2(-11,-137),hair,2,true)
	draw_line(Vector2(8,-137),Vector2(15,-135),hair,2,true)
	draw_arc(Vector2(1,-123),8,.3,PI-.3,16,INK,1.5,true)
	draw_line(Vector2(0,-128),Vector2(-1,-122),Color(p.skin).darkened(.22),1.5,true)
	draw_line(Vector2(-15,-66),Vector2(11,-66),shirt.lightened(.3),3,true)
	if p.style==0: draw_circle(Vector2(9,-87),4,Color("fff2ca"))
	elif p.style==2: draw_line(Vector2(-18,-79),Vector2(17,-79),Color("f4e6c1"),6,true)
	draw_set_transform(Vector2.ZERO)
func shadow_ellipse(center: Vector2,radii: Vector2,color: Color) -> void:
	var points := PackedVector2Array()
	for i in range(40): points.append(center+Vector2(cos(i*TAU/40)*radii.x,sin(i*TAU/40)*radii.y))
	draw_colored_polygon(points,color)
