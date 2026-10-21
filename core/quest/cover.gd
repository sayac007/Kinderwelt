extends Control
const Tracks=preload("res://core/quest/tracks.gd")
const Art=preload("res://core/quest/art.gd")
var track:="wiener_blut"
func _ready() -> void: mouse_filter=MOUSE_FILTER_IGNORE
func _draw() -> void:
	var data: Dictionary=Tracks.ITEMS[track]
	var paper:=Color(data.color)
	var box:=StyleBoxFlat.new();box.bg_color=paper;box.set_corner_radius_all(24)
	draw_style_box(box,Rect2(Vector2(5,5),size-Vector2(10,10)))
	var index: int=Tracks.ITEMS.keys().find(track)
	for i in range(3):
		draw_arc(Vector2(size.x*.2,size.y*.5),size.y*(.25+i*.12),-.7,2.3,32,Color(1,1,1,.25),4,true)
	var motif: String={"gear":"robot","moon":"moon","leaf":"leaf","drop":"fish","sun":"sun"}.get(data.icon,"star")
	var side:=minf(size.x-24,size.y-18)
	Art.object(self,motif,Rect2((size-Vector2.ONE*side)/2,Vector2.ONE*side))
	for i in range(index%4+1):Art.star(self,Vector2(17+i*13,size.y-16),4,Color("fff4cd"))
