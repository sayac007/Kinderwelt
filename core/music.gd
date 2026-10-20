extends Node
# Two voices permit crossfades. Themes can later resolve to a different instrument bank.
var store: RefCounted
var players: Array[AudioStreamPlayer] = []
var active := 0
var world := ""
var transition: Tween
const BANKS := {"retro":"res://assets/music/"}
var palette := "retro"
var suspended := false

func _ready() -> void:
	for i in range(2):
		var player := AudioStreamPlayer.new()
		player.volume_db = -60
		add_child(player)
		players.append(player)

func set_world(next: String) -> void:
	if next == world: return
	world = next
	if not is_inside_tree() or store == null: return
	if transition: transition.kill()
	var previous := active
	active = 1-active
	var player := players[active]
	player.stop()
	var registry = preload("res://games/adventure/tracks.gd").ITEMS
	var path: String = registry[next].path if registry.has(next) else str(BANKS.get(palette,BANKS.retro))+next+".wav"
	var track := load(path) as AudioStreamWAV
	if track == null: return
	track = track.duplicate()
	track.loop_mode = AudioStreamWAV.LOOP_FORWARD
	track.loop_begin = 0
	track.loop_end = roundi(track.get_length()*track.mix_rate)
	player.stream = track
	player.volume_db = -60
	if store.data.muted or float(store.data.music_volume)<=0: return
	player.play()
	transition = create_tween().set_parallel()
	transition.tween_property(player,"volume_db",linear_to_db(float(store.data.music_volume)),0.7)
	transition.tween_property(players[previous],"volume_db",-60,0.7)
	transition.chain().tween_callback(players[previous].stop)

func sync_settings() -> void:
	if store == null or players.is_empty(): return
	if transition: transition.kill()
	for i in range(2):
		if i!=active or store.data.muted or float(store.data.music_volume)<=0:
			players[i].stop()
		else:
			players[i].volume_db=linear_to_db(float(store.data.music_volume))
			if players[i].stream!=null and not players[i].playing: players[i].play()

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_PAUSED:
		suspended = true
		for player in players: player.stream_paused = true
	elif what == NOTIFICATION_APPLICATION_RESUMED:
		suspended = false
		for player in players: player.stream_paused = false
		sync_settings()

func _exit_tree() -> void:
	if transition: transition.kill()
	for player in players:
		player.stop()
		player.stream = null
