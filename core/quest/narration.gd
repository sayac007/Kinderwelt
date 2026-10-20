extends AudioStreamPlayer
# Only bundled clips. No microphone, OS/cloud TTS, or network at runtime.
var store: RefCounted
var music: Node
var clip := ""
func configure(saved: RefCounted,background: Node) -> void:
	store = saved
	music = background
	finished.connect(release_duck)
func play_clip(id: String,automatic := false) -> bool:
	cancel()
	if store.data.muted or float(store.data.voice_volume)<=0 or (automatic and not store.data.voice_auto): return false
	var path := "res://assets/voice/"+id+".ogg"
	if not ResourceLoader.exists(path): return false
	clip = id
	stream = load(path)
	volume_db = linear_to_db(float(store.data.voice_volume))
	music.set_ducked(true)
	play()
	return true
func release_duck() -> void:
	if is_instance_valid(music): music.set_ducked(false)
func cancel() -> void:
	stop()
	stream = null
	clip = ""
	release_duck()
func sync_settings() -> void:
	if store.data.muted or float(store.data.voice_volume)<=0: cancel()
	else: volume_db = linear_to_db(float(store.data.voice_volume))
func _notification(what: int) -> void:
	if what==NOTIFICATION_APPLICATION_PAUSED: stream_paused = true
	elif what==NOTIFICATION_APPLICATION_RESUMED: stream_paused = false
func _exit_tree() -> void:
	cancel()
