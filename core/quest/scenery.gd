extends RefCounted
# One atlas for four new worlds; all moving props are drawn/reused at runtime.
const IDS := ["mountains","home","castle","tree","seabed","city","moon"]
const CHOICES := ["auto","mountains","home","castle","tree","seabed","city","moon"]
const ATLAS = preload("res://assets/quest/adventure-worlds.png")
const BACKGROUNDS = {"mountains":preload("res://assets/quest/landscape.png"),"home":preload("res://assets/quest/home.png"),"castle":preload("res://assets/quest/castle.png")}
static func choice(data: Dictionary,subject: String) -> String:
	return data.subject_sceneries.get(subject,"auto")
static func resolve(data: Dictionary,subject: String,page: int) -> String:
	var selected := choice(data,subject)
	if selected!="auto": return selected
	return IDS[(preload("res://games/quest/progress.gd").SUBJECTS.find(subject)+page)%IDS.size()]
static func texture(id: String) -> Texture2D:
	return BACKGROUNDS.get(id,ATLAS)
static func region(id: String) -> Rect2:
	var image := texture(id)
	if BACKGROUNDS.has(id): return Rect2(Vector2.ZERO,image.get_size())
	var index := IDS.find(id)-3
	var cell := ATLAS.get_size()/2
	return Rect2(Vector2(index%2,index/2)*cell,cell)
static func paint(canvas: CanvasItem,id: String,rect: Rect2,tint := Color.WHITE,elevation: float=-1.0) -> void:
	var crop := region(id)
	var fit := maxf(rect.size.x/crop.size.x,rect.size.y/crop.size.y)
	if id=="tree" and elevation>=0:fit*=1.35
	var visible := rect.size/fit
	var anchor:=Vector2(.78,.5) if id=="moon" else Vector2(.67,.5) if id=="seabed" else Vector2(.5,1-elevation) if id=="tree" and elevation>=0 else Vector2(.5,.5)
	crop.position+=(crop.size-visible)*anchor
	crop.size=visible
	canvas.draw_texture_rect_region(texture(id),rect,crop,tint)
