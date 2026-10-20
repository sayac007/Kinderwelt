extends Control
const ATLAS = preload("res://assets/quest/icons.png")
const REGIONS := [Rect2(0,0,545,510),Rect2(545,0,480,510),Rect2(1025,0,511,510),Rect2(0,512,545,512),Rect2(545,512,480,512),Rect2(1025,512,511,512)]
var cell := Vector2i.ZERO
func _ready() -> void: mouse_filter = MOUSE_FILTER_IGNORE
func _draw() -> void:
	draw_texture_rect_region(ATLAS,Rect2(Vector2.ZERO,size),REGIONS[cell.y*3+cell.x])
