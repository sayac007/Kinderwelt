extends RefCounted
const INK := Color("293b4c")
const OBJECTS = preload("res://assets/quest/objects.png")
const SCIENCE_A = preload("res://assets/quest/science-a.png")
const SCIENCE_B = preload("res://assets/quest/science-b.png")
const SCIENCE_IDS := ["gear","wheel","bridge","magnet","bulb","battery","scissors","hammer","screwdriver","lever","pulley","helmet","bird","butterfly","bee","frog","turtle","cat","seed","roots","mushroom","egg","nest","worm","water","ice","steam","salt","sand","oil","glass","metal","wood","paper","fabric","soap","eye","ear","nose","tongue","hand","heart","lungs","brain","bone","tooth","foot","stomach","globe","map","compass","mountain","river","island","cloud","rain","snow","desert","forest","sea"]
const REGIONS := {"apple":Rect2(18,0,349,334),"leaf":Rect2(399,0,358,334),"star":Rect2(783,0,358,334),"moon":Rect2(1164,0,360,334),"sun":Rect2(20,339,350,296),"ball":Rect2(405,340,350,296),"house":Rect2(785,341,350,297),"mouse":Rect2(1164,340,360,299),"robot":Rect2(20,636,350,370),"flower":Rect2(405,649,350,357),"fish":Rect2(784,643,350,363),"tree":Rect2(1164,643,360,363)}
static var face: FontVariation
static func font() -> Font:
	if face==null:
		face = FontVariation.new()
		face.base_font = preload("res://assets/quest/Nunito.ttf")
		face.variation_opentype = {2003265652:700} # OpenType wght axis tag
	return face
static func text(canvas: CanvasItem,word: String,center: Vector2,px: int,color := INK) -> void:
	var f := font()
	canvas.draw_string(f,center-Vector2(f.get_string_size(word,HORIZONTAL_ALIGNMENT_LEFT,-1,px).x/2.0,-px*.34),word,HORIZONTAL_ALIGNMENT_LEFT,-1,px,color)
static func object(canvas: CanvasItem,id: String,rect: Rect2,tint := Color.WHITE) -> void:
	if REGIONS.has(id):
		canvas.draw_texture_rect_region(OBJECTS,rect,REGIONS[id],tint)
		return
	var index := SCIENCE_IDS.find(id)
	if index>=0:
		var atlas: Texture2D = SCIENCE_A if index<30 else SCIENCE_B
		index = index%30
		var cell := Vector2(atlas.get_width()/6.0,atlas.get_height()/5.0)
		var region := Rect2(Vector2(index%6,index/6)*cell+Vector2.ONE*3,cell-Vector2.ONE*6)
		var fit := region.size*minf(rect.size.x/region.size.x,rect.size.y/region.size.y)
		canvas.draw_texture_rect_region(atlas,Rect2(rect.get_center()-fit/2,fit),region,tint)

static func has_object(id: String) -> bool:
	return REGIONS.has(id) or id in SCIENCE_IDS

static func star(canvas: CanvasItem,center: Vector2,radius: float,color: Color) -> void:
	var points := PackedVector2Array()
	for i in range(10):
		var a := i*PI/5-PI/2
		points.append(center+Vector2(cos(a),sin(a))*radius*(1.0 if i%2==0 else .48))
	canvas.draw_colored_polygon(points,color)
static func empty_star(canvas: CanvasItem,center: Vector2,radius: float) -> void:
	var points := PackedVector2Array()
	for i in range(11):
		var a := i*PI/5-PI/2
		points.append(center+Vector2(cos(a),sin(a))*radius*(1.0 if i%2==0 else .48))
	canvas.draw_polyline(points,Color("536576"),2,true)
