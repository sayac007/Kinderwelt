extends RefCounted
const PATH = "user://progress.json"
var data: Dictionary = defaults()

static func defaults() -> Dictionary:
	return {"schema": 1, "completed": {}, "muted": false, "reduced_motion": false}

func load_save() -> void:
	data = defaults()
	if not FileAccess.file_exists(PATH):
		return
	var parser := JSON.new()
	if parser.parse(FileAccess.get_file_as_string(PATH)) != OK:
		return
	var value = parser.data
	if value is Dictionary and value.get("schema") == 1 and value.get("completed") is Dictionary and value.get("muted") is bool and value.get("reduced_motion") is bool:
		data = value

func persist() -> Error:
	var file = FileAccess.open(PATH + ".tmp", FileAccess.WRITE)
	if file == null:
		return FileAccess.get_open_error()
	file.store_string(JSON.stringify(data))
	file.close()
	return DirAccess.rename_absolute(PATH + ".tmp", PATH)

func reset() -> Error:
	data = defaults()
	return persist()
