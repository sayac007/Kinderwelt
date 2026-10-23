extends AudioStreamPlayer
# Only bundled clips, always in the selected language.
var store: RefCounted
var music: Node
var clip := ""
var catalogs := {}
var queue: Array[String] = []
var pending_feedback := ""
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
	music.set_ducked(true)
	play_next()
	return true
func speak_feedback(id: String) -> void:
	# A quick answer must not cut off the end of the spoken question.
	if playing or not queue.is_empty():
		pending_feedback=id.trim_prefix("quest/")
	else: play_clip(id)
func play_next() -> void:
	if queue.is_empty() and not pending_feedback.is_empty():
		var next_id := pending_feedback
		pending_feedback=""
		var path := resolve(next_id,store.data.locale)
		if not path.is_empty():
			queue.append(path)
			clip="quest/"+next_id
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
	pending_feedback=""
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
