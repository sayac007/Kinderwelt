extends AudioStreamPlayer
# Original synthesized tones; no recording, speech engine or network.
var store: RefCounted
var music: Node

func configure(saved: RefCounted) -> void:
	store = saved
	music = preload("res://core/music.gd").new()
	music.store = store
	add_child(music)
	sync_settings()

func set_world(world: String) -> void:
	var registry = preload("res://core/quest/tracks.gd")
	# Walking between subjects does not restart the selected playlist.
	if not music.world.is_empty(): return
	var next: String = store.data.music_track
	if not registry.ITEMS.has(next): next = registry.resolve(world)
	music.set_world(next)


func sync_settings() -> void:
	if store == null: return
	volume_db = linear_to_db(maxf(float(store.data.effects_volume),0.0001))-5
	if store.data.muted or float(store.data.effects_volume)<=0: stop()
	if music != null: music.sync_settings()

func _process(_delta: float) -> void:
	if store != null and store.data.muted:
		stop()
		music.sync_settings()
func cue(success: bool = false, tone: int = -1) -> void:
	if store != null and (store.data.muted or float(store.data.effects_volume)<=0): return
	stop()
	var wav := AudioStreamWAV.new()
	wav.format = AudioStreamWAV.FORMAT_16_BITS
	wav.mix_rate = 22050
	var bytes := PackedByteArray()
	var duration := 0.35 if success else 0.18
	for i in range(int(22050 * duration)):
		var t := float(i) / 22050.0
		var frequency := 440.0 * pow(2.0, clampi(tone, 0, 7) / 12.0) if tone >= 0 else (660.0 if success else 440.0)
		var signal_value := sin(TAU * frequency * t)
		if success: signal_value = (signal_value+sin(TAU*frequency*1.25*t)+sin(TAU*frequency*1.5*t))/2.0
		var sample := int(signal_value * 5000 * (1.0 - t / duration))
		bytes.append(sample & 255)
		bytes.append((sample >> 8) & 255)
	wav.data = bytes
	stream = wav
	play()

func _exit_tree() -> void:
	stop()
	stream = null
