extends RefCounted
const Learning = preload("res://core/learning_catalog.gd")

static func modules() -> Array:
	var value = JSON.parse_string(FileAccess.get_file_as_string("res://content/modules.json"))
	return value if value is Array else []

static func level(entry: Dictionary) -> Dictionary:
	var value = JSON.parse_string(FileAccess.get_file_as_string(entry.level))
	if not value is Dictionary or value.get("schema") != 1 or value.get("module") != entry.id or not value.get("target") is float or value.target < 1:
		return {}
	return value

static func levels(entry: Dictionary) -> Array:
	if entry.has("levels"): return Learning.load_levels(entry)
	var single := level(entry)
	return [] if single.is_empty() else [single]
