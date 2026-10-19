extends RefCounted

static func modules() -> Array:
	var value = JSON.parse_string(FileAccess.get_file_as_string("res://content/modules.json"))
	return value if value is Array else []

static func level(entry: Dictionary) -> Dictionary:
	var value = JSON.parse_string(FileAccess.get_file_as_string(entry.level))
	if not value is Dictionary or value.get("schema") != 1 or value.get("module") != entry.id or not value.get("target") is float or value.target < 1:
		return {}
	return value
