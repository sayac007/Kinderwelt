extends AudioStreamPlayer
# Only bundled clips. German learning targets keep German pronunciation.
var store: RefCounted
var music: Node
var clip := ""
var catalogs := {}
var queue: Array[String] = []
func configure(saved: RefCounted,background: Node) -> void:
	store = saved
	music = background
	finished.connect(on_finished)
func resolve(id: String,locale: String) -> String:
	if not catalogs.has(locale):
		var path := "res://assets/voice/quest/"+locale+"/manifest.json"
		if not FileAccess.file_exists(path): return ""
		var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
		var entries := {}
		for entry in data.clips: entries[entry.id]=entry.file
		catalogs[locale]=entries
	if not catalogs[locale].has(id): return ""
	var filename: String = catalogs[locale][id]
	return "res://assets/voice/quest/"+locale+"/"+filename
func play_clip(id: String,automatic := false) -> bool:
	cancel()
	if store.data.muted or float(store.data.voice_volume)<=0 or (automatic and not store.data.voice_auto): return false
	var basename := id.trim_prefix("quest/")
	var path := resolve(basename,store.data.locale)
	if path.is_empty() or not ResourceLoader.exists(path): return false
	clip = id
	queue.append(path)
	if store.data.locale!="de" and basename.begins_with("german_"):
		var german := resolve(basename,"de")
		if not german.is_empty(): queue.append(german)
	music.set_ducked(true)
	play_next()
	return true
func play_next() -> void:
	if queue.is_empty():
		stream = null
		clip = ""
		release_duck()
		return
	stream = load(queue.pop_front())
	volume_db = linear_to_db(float(store.data.voice_volume))
	play()
func on_finished() -> void: play_next()
func release_duck() -> void:
	if is_instance_valid(music): music.set_ducked(false)
func cancel() -> void:
	stop()
	queue.clear()
	stream = null
	clip = ""
	release_duck()
func sync_settings() -> void:
	if store.data.muted or float(store.data.voice_volume)<=0: cancel()
	else: volume_db = linear_to_db(float(store.data.voice_volume))
func _notification(what: int) -> void:
	if what==NOTIFICATION_APPLICATION_PAUSED: stream_paused = true
	elif what==NOTIFICATION_APPLICATION_RESUMED: stream_paused = false
func _exit_tree() -> void: cancel()
