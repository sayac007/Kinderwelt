extends SceneTree
# The same 60-frame real-scene startup smoke test, followed by the production
# close handler. --quit-after bypasses it and tears down active streaming audio.
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var app: Control = load(ProjectSettings.get_setting("application/run/main_scene")).instantiate()
	root.add_child(app)
	for i in range(60): await process_frame
	if not is_instance_valid(app.grid) or app.grid.get_child_count()!=5:
		push_error("Startup did not create five playable places")
		quit(1)
		return
	print("BOOT: 60 frames; production audio shutdown")
	await app.shutdown()
