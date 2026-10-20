extends Control
# Small line-and-wash illustrations. Original contours, no third-party imagery.
var place := "logic"
const INK := Color("354b53")
func _ready() -> void: mouse_filter = Control.MOUSE_FILTER_IGNORE
func line(a: Vector2,b: Vector2,c: Color,w := 5.0) -> void:
	draw_line(a,b,INK,w+3,true)
	draw_line(a,b,c,w,true)
func poly(points: PackedVector2Array,c: Color) -> void:
	draw_colored_polygon(points,c)
	draw_polyline(points+PackedVector2Array([points[0]]),INK,2.5,true)
func leaf(at: Vector2,s := 1.0) -> void:
	poly(PackedVector2Array([at,at+Vector2(-20,-15)*s,at+Vector2(-24,-32)*s,at+Vector2(-4,-24)*s]),Color("7da16a"))
func _draw() -> void:
	var k := minf(size.x/180,size.y/130)
	draw_set_transform(Vector2((size.x-180*k)/2,(size.y-130*k)/2),0,Vector2(k,k))
	poly(PackedVector2Array([Vector2(2,111),Vector2(25,80),Vector2(62,73),Vector2(106,90),Vector2(154,79),Vector2(178,111),Vector2(155,123),Vector2(25,125)]),Color("a6bc80"))
	match place:
		"logic":
			poly(PackedVector2Array([Vector2(49,124),Vector2(66,88),Vector2(126,84),Vector2(142,124)]),Color("75b8c9"))
			for i in range(7):
				var x := 27+i*20
				var y := 78-sin(i*PI/6)*14
				line(Vector2(x,y-25),Vector2(x,y+22),Color("b9885d"),6)
				poly(PackedVector2Array([Vector2(x-8,y),Vector2(x+9,y-1),Vector2(x+9,y+14),Vector2(x-9,y+15)]),Color("dbb17d"))
			line(Vector2(26,53),Vector2(88,38),Color("c69662"),4)
			line(Vector2(88,38),Vector2(147,54),Color("c69662"),4)
		"math":
			poly(PackedVector2Array([Vector2(35,70),Vector2(147,70),Vector2(140,113),Vector2(40,113)]),Color("d7a16a"))
			for x in [43,138]: line(Vector2(x,28),Vector2(x,114),Color("946e50"),6)
			poly(PackedVector2Array([Vector2(28,36),Vector2(43,17),Vector2(140,17),Vector2(155,36)]),Color("e8b852"))
			for i in range(7):
				if i%2==0: draw_line(Vector2(37+i*16,28),Vector2(39+i*16,45),Color("b95c4d"),13,true)
			for i in range(5):
				draw_circle(Vector2(54+i*18,63-abs(i-2)*2),10,Color("c7614e"))
				leaf(Vector2(54+i*18,56),.35)
		"language":
			poly(PackedVector2Array([Vector2(20,55),Vector2(82,40),Vector2(90,49),Vector2(95,40),Vector2(159,51),Vector2(159,110),Vector2(95,99),Vector2(90,107),Vector2(82,99),Vector2(20,115)]),Color("fff2d2"))
			line(Vector2(90,50),Vector2(90,103),Color("be986b"),2)
			for y in [81,91]: draw_line(Vector2(34,y),Vector2(69,y-5),Color("946f83"),3,true)
			line(Vector2(120,85),Vector2(120,61),Color("729568"),4)
			leaf(Vector2(120,77),.65)
			draw_circle(Vector2(128,39),16,Color("e9b94d"))
		"autonomy":
			poly(PackedVector2Array([Vector2(30,65),Vector2(86,24),Vector2(150,65),Vector2(150,114),Vector2(30,114)]),Color("c3dacb"))
			line(Vector2(24,65),Vector2(86,19),Color("6b958d"),7)
			line(Vector2(86,19),Vector2(157,65),Color("6b958d"),7)
			line(Vector2(86,25),Vector2(86,114),Color("e9eee2"),4)
			poly(PackedVector2Array([Vector2(62,90),Vector2(113,90),Vector2(105,120),Vector2(68,120)]),Color("c87d54"))
			line(Vector2(87,91),Vector2(87,59),Color("6b935b"),5)
			leaf(Vector2(87,75),.8)
			leaf(Vector2(110,69),.75)
		"social":
			for i in range(3):
				var x := 18+i*54
				poly(PackedVector2Array([Vector2(x,61),Vector2(x+23,40),Vector2(x+46,60),Vector2(x+46,111),Vector2(x,111)]),Color(["e7c697","c3b7d2","b7d1c5"][i]))
				line(Vector2(x-3,62),Vector2(x+23,36),Color("b37865"),5)
				line(Vector2(x+23,36),Vector2(x+49,62),Color("b37865"),5)
				draw_rect(Rect2(x+17,85,14,26),Color("6d8c8d"))
	draw_set_transform(Vector2.ZERO)
