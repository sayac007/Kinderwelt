extends Node
# Bounded two-player cache; both original WAVs and compressed Vorbis are supported.
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
func target_db() -> float:
	return linear_to_db(maxf(.0001,float(store.data.music_volume)))+(-13.0 if ducked else 0.0)
func set_ducked(value: bool) -> void:
	if value==ducked: return
	ducked = value
	if is_inside_tree() and store!=null and not players.is_empty():
		# Cancel an in-progress crossfade too: narration always wins over its target.
		sync_settings()
func set_world(next: String) -> void:
	if next==world: return
	if not is_inside_tree() or store==null: return
	var registry = preload("res://core/quest/tracks.gd").ITEMS
	if not registry.has(next): return
	var path: String = registry[next].path
	if not ResourceLoader.exists(path): return
	var track := load(path) as AudioStream
	if track==null: return
	track = track.duplicate()
	if track is AudioStreamWAV:
		track.loop_mode = AudioStreamWAV.LOOP_FORWARD
		track.loop_begin = 0
		track.loop_end = roundi(track.get_length()*track.mix_rate)
	elif track is AudioStreamOggVorbis:
		track.loop = true
		track.loop_offset = 0
	world = next
	if transition: transition.kill()
	var previous := active
	active = 1-active
	var player := players[active]
	player.stop()
	player.stream = track
	player.volume_db = -60
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
