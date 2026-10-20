extends RefCounted
const PATH = "user://progress.json"
var data: Dictionary = defaults()

static func defaults() -> Dictionary:
	return {"schema": 1, "completed": {}, "muted": false, "reduced_motion": false, "music_volume": 0.35, "effects_volume": 0.6, "text_scale": 1.0, "hero":"mina", "music_track":"adventure_workshop", "music_locked":false, "music_shuffle":false, "voice_auto":true, "voice_volume":0.8, "show_instructions":false, "water":{}, "water_tier":0}

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
		var text_size = data.get("text_scale",1.0)
		data.text_scale = clampf(float(text_size),1.0,1.15) if (text_size is float or text_size is int) and is_finite(float(text_size)) else 1.0
		for key in ["music_volume","effects_volume","voice_volume"]:
			var volume = data.get(key, defaults()[key])
			data[key] = clampf(float(volume),0.0,1.0) if (volume is float or volume is int) and is_finite(float(volume)) else defaults()[key]

		for key in ["music_locked","music_shuffle","voice_auto","show_instructions"]:
			if not data.get(key) is bool: data[key] = defaults()[key]
		for key in ["hero","music_track"]:
			if not data.get(key) is String: data[key] = defaults()[key]
		if not preload("res://core/modern/hero.gd").PEOPLE.has(data.hero): data.hero = "mina"
		if not data.get("water") is Dictionary: data.water = {}
		var tier = data.get("water_tier",0)
		data.water_tier = clampi(int(tier),0,2) if (tier is int or tier is float) and is_finite(float(tier)) else 0

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
