extends RefCounted
const PATH="user://progress.json"
const Progress=preload("res://games/quest/progress.gd")
var data: Dictionary=defaults()
static func defaults() -> Dictionary:
	return {"schema":2,"muted":false,"reduced_motion":false,"music_volume":.35,"effects_volume":.6,"voice_volume":.8,"voice_auto":true,"text_scale":1.0,"hero":"mischa","music_track":"wiener_blut","music_locked":false,"music_shuffle":false,"quest":Progress.clean(null)}
static func clean(value: Variant) -> Dictionary:
	var result:=defaults()
	if not value is Dictionary: return result
	# Only current whitelisted preferences/tasks are retained, never obsolete data.
	for key in ["muted","reduced_motion","voice_auto","music_locked","music_shuffle"]:
		if value.get(key) is bool: result[key]=value[key]
	for key in ["music_volume","effects_volume","voice_volume","text_scale"]:
		var v: Variant=value.get(key)
		if (v is int or v is float) and is_finite(float(v)):
			result[key]=clampf(float(v),1,1.15) if key=="text_scale" else clampf(float(v),0,1)
	if value.get("hero") is String:
		var id: String = {"mina":"mischa","leo":"du","sam":"mama","jule":"katze"}.get(value.hero,value.hero)
		if id in ["mischa","du","mama","katze"]: result.hero=id
	if value.get("music_track") is String and preload("res://core/quest/tracks.gd").ITEMS.has(value.music_track): result.music_track=value.music_track
	else: result.music_locked=false
	result.quest=Progress.clean(value.get("quest"))
	return result
func load_save() -> void:
	data=defaults()
	if not FileAccess.file_exists(PATH): return
	data=clean(JSON.parse_string(FileAccess.get_file_as_string(PATH)))
func persist() -> Error:
	var file:=FileAccess.open(PATH+".tmp",FileAccess.WRITE)
	if file==null: return FileAccess.get_open_error()
	file.store_string(JSON.stringify(data));file.close()
	return DirAccess.rename_absolute(PATH+".tmp",PATH)
func reset() -> Error:
	data=defaults();return persist()
