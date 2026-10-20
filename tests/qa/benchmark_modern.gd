extends SceneTree
var output := ""
var samples := []
func _initialize() -> void:
	output = OS.get_environment("KINDERWELT_PERF_OUTPUT")
	call_deferred("run")
func run() -> void:
	var start := Time.get_ticks_usec()
	root.size = Vector2i(360,800)
	var app: Control = load("res://core/main.tscn").instantiate()
	root.add_child(app)
	await process_frame
	await process_frame
	var startup_ms := (Time.get_ticks_usec()-start)/1000.0
	print("MODERN READY: two project frames")
	app.store.reset()
	app.store.data.muted = true
	app.audio.sync_settings()
	for name in ["heroes","musicbox","open_water","hub","open_water","hub"]:
		start = Time.get_ticks_usec()
		app.call(name)
		await process_frame
		await process_frame
		samples.append({"scene":name,"ready_ms":(Time.get_ticks_usec()-start)/1000.0,"static_memory_bytes":OS.get_static_memory_usage(),"resources":Performance.get_monitor(Performance.OBJECT_RESOURCE_COUNT)})
	app.store.data.muted = false
	app.audio.sync_settings()
	var max_voices := 0
	for id in preload("res://core/modern/tracks.gd").ITEMS:
		start = Time.get_ticks_usec()
		app.audio.music.set_world(id)
		var count := 0
		for p in app.audio.music.players:
			if p.stream!=null: count += 1
		max_voices = maxi(max_voices,count)
		samples.append({"track":id,"load_ms":(Time.get_ticks_usec()-start)/1000.0,"active_stream_slots":count,"static_memory_bytes":OS.get_static_memory_usage()})
	app.audio.music._notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	var paused: bool = app.audio.music.suspended
	app.audio.music._notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	var resumed: bool = not app.audio.music.suspended
	app.open_water()
	app.modern_view.model.rotate(5)
	app.modern_view.model.rotate(6)
	app.modern_view.turn_water()
	var frames := []
	for i in range(90):
		start = Time.get_ticks_usec()
		await process_frame
		frames.append((Time.get_ticks_usec()-start)/1000.0)
	frames.sort()
	var report := {"scope":"Automated desktop engine timings; no Android performance/latency claim","renderer":DisplayServer.get_name(),"audio_driver":"Dummy; no hardware output measurement","startup_to_two_frames_ms":startup_ms,"samples":samples,"frame_intervals_ms":{"median":frames[45],"p95":frames[85],"max":frames[-1]},"max_music_stream_slots":max_voices,"background_state_paused":paused,"background_state_resumed":resumed}
	var f := FileAccess.open(output,FileAccess.WRITE);f.store_string(JSON.stringify(report,"  "));f.close()
	app.narration.cancel()
	app.free()
	await create_timer(.5).timeout
	print("MODERN PERFORMANCE: measured, bounded music slots ",max_voices)
	quit(0 if max_voices<=2 and paused and resumed else 1)
