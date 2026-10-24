extends Control
var texture: Texture2D
func _ready() -> void:
	mouse_filter=MOUSE_FILTER_IGNORE
func _draw() -> void:
	# Two mattes make leftover white rectangles visible without erasing white fur.
	for y in range(ceili(size.y/24.0)):
		for x in range(ceili(size.x/24.0)):
			var dark := x*24>=size.x/2
			var color := Color("304657") if dark else Color("f2eee5")
			if (x+y)%2==0: color=color.lightened(.12) if dark else color.darkened(.08)
			draw_rect(Rect2(x*24,y*24,minf(24,size.x-x*24),minf(24,size.y-y*24)),color)
	if texture!=null:
		var fitted := texture.get_size()*minf((size.x-24)/texture.get_width(),(size.y-24)/texture.get_height())
		draw_texture_rect(texture,Rect2((size-fitted)/2,fitted),false)
