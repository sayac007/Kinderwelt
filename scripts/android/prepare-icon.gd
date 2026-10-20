extends SceneTree

func _initialize() -> void:
	var image := Image.new()
	var result := image.load_svg_from_string(FileAccess.get_file_as_string("res://assets/icons/kinderwelt.svg"))
	if result == OK:
		result = image.save_png("res://docs/store-assets/icon-512.png")
	if result != OK:
		push_error("Could not generate store icon")
	quit(result)
