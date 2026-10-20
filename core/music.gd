extends Node
signal track_changed(id: String)
# Bounded two-player cache; tracks advance when their actual audio ends.
var store: RefCounted
var players: Array[AudioStreamPlayer] = []
var active := 0
var world := ""
var transition: Tween
var suspended := false
var ducked := false
func _ready() -> void:
	for i in range(2):
		var player := AudioStreamPlayer.new()
		player.volume_db = -60
		add_child(player)
		players.append(player)
		player.finished.connect(func(): on_finished(i))
func target_db() -> float:
	return linear_to_db(maxf(.0001,float(store.data.music_volume)))+(-13.0 if ducked else 0.0)
func set_ducked(value: bool) -> void:
	if value==ducked: return
	ducked = value
	if is_inside_tree() and store!=null and not players.is_empty():
		# Cancel an in-progress crossfade too: narration always wins over its target.
		sync_settings()
func set_world(next: String,restart := false) -> void:
	if next==world and not restart: return
	if not is_inside_tree() or store==null: return
	var registry = preload("res://core/quest/tracks.gd").ITEMS
	if not registry.has(next): return
	var path: String = registry[next].path
	if not ResourceLoader.exists(path): return
	var track := load(path) as AudioStream
	if track==null: return
	track = track.duplicate()
	if track is AudioStreamWAV:
		track.loop_mode = AudioStreamWAV.LOOP_DISABLED
	elif track is AudioStreamOggVorbis:
		track.loop = false
	world = next
	store.data.music_track = next
	if transition: transition.kill()
	var previous := active
	active = 1-active
	var player := players[active]
	player.stop()
	player.stream = track
	player.volume_db = -60
	track_changed.emit(next)
	if store.data.muted or float(store.data.music_volume)<=0:
		players[previous].stop()
		players[previous].stream = null
		return
	player.play()
	player.stream_paused = suspended
	transition = create_tween().set_parallel()
	transition.tween_property(player,"volume_db",target_db(),.6)
	transition.tween_property(players[previous],"volume_db",-60,.6)
	transition.chain().tween_callback(func(): players[previous].stop(); players[previous].stream = null)
func on_finished(index: int) -> void:
	if index!=active or store==null or suspended or store.data.muted or float(store.data.music_volume)<=0: return
	var id: String = preload("res://core/quest/tracks.gd").next(world,1,store.data.music_shuffle,store.data.music_locked)
	set_world(id,true)
	if store.persist()!=OK: push_warning("Music preference could not be saved")
func sync_settings() -> void:
	if store==null or players.is_empty(): return
	if transition: transition.kill()
	for i in range(2):
		if i!=active or store.data.muted or float(store.data.music_volume)<=0:
			players[i].stop()
			if i!=active: players[i].stream = null
		else:
			players[i].volume_db = target_db()
			if players[i].stream!=null and not players[i].playing: players[i].play()
			players[i].stream_paused = suspended
func _notification(what: int) -> void:
	if what==NOTIFICATION_APPLICATION_PAUSED:
		suspended = true
		for player in players: player.stream_paused = true
	elif what==NOTIFICATION_APPLICATION_RESUMED:
		suspended = false
		for player in players: player.stream_paused = false
		sync_settings()
func shutdown() -> void:
	if transition: transition.kill()
	for player in players:
		player.stop()
		player.stream = null

func _exit_tree() -> void:
	shutdown()
