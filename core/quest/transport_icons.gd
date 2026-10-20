extends RefCounted
static func apply(button: Button,id: String,width := 28) -> void:
	button.icon = load("res://assets/quest/ui/"+id+".svg")
	button.add_theme_constant_override("icon_max_width",width)
	button.expand_icon = true
	button.icon_alignment = HORIZONTAL_ALIGNMENT_LEFT
