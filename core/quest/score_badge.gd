extends Control
const Art = preload("res://core/quest/art.gd")
var stars := 0
var points := 0
var shown := 0.0
var pulse := 0.0
var reduced_motion := false
var caption := "Punkte"
var reward := 10
func _ready() -> void:
	mouse_filter = MOUSE_FILTER_IGNORE
	clip_contents = true
func set_total(total: int,animate := false,total_points := -1,earned := 10) -> void:
	var next_points:=total*10 if total_points<0 else total_points
	var changed := next_points>points
	stars=total;points=next_points;reward=earned
	if animate and changed: pulse=1.3
	if not animate or reduced_motion: shown=points
	queue_redraw()
func _process(delta: float) -> void:
	if pulse<=0 and shown==points: return
	pulse=maxf(0,pulse-delta)
	shown=move_toward(shown,points,maxf(100,absf(points-shown)*6)*delta) if not reduced_motion else float(points)
	queue_redraw()
func _draw() -> void:
	var box := StyleBoxFlat.new()
	box.bg_color=Color("5c469c").lerp(Color("147c8a"),minf(1,pulse))
	box.border_color=Color("ffd66b");box.set_border_width_all(2);box.set_corner_radius_all(22)
	draw_style_box(box,Rect2(Vector2.ZERO,size))
	var bounce := sin(pulse*PI)*2 if pulse>0 and not reduced_motion else 0.0
	Art.star(self,Vector2(23,20+bounce),12,Color("ffe280"))
	Art.text(self,str(stars),Vector2(23,43),12,Color("fff6c9"))
	var center := Vector2((size.x+36)/2,21-bounce)
	var number:=str(roundi(shown))
	var px:=25
	while px>13 and Art.font().get_string_size(number,HORIZONTAL_ALIGNMENT_LEFT,-1,px).x>size.x-62: px-=1
	Art.text(self,number,center,px,Color.WHITE)
	Art.text(self,caption if pulse<=0 else "+"+str(reward),Vector2(center.x,43),12,Color("e8fff4") if pulse<=0 else Color("ffe28b"))
