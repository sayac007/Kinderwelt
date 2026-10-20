extends SceneTree
var checks := 0
var failures := 0

func check(value: bool, message: String) -> void:
	checks += 1
	if not value:
		failures += 1
		push_error(message)

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var catalog = load("res://core/catalog.gd")
	var entries = catalog.modules()
	check(entries.size() == 5, "Five modules registered")
	var app = load("res://core/main.tscn").instantiate()
	root.add_child(app)
	await process_frame
	check(app.grid.get_child_count() == 5, "Hub has five buttons")
	for entry in entries.slice(2):
		# Retain every original assertion for the supported foundation fallback.
		# The new registered runtimes are exercised in tests/scenarios.gd.
		var foundation_entry: Dictionary = entry.duplicate()
		foundation_entry.erase("runtime")
		foundation_entry.erase("levels")
		check(not catalog.level(entry).is_empty(), "Valid level: " + entry.id)
		app.open_module(foundation_entry)
		check(app.taps == 0, "Fresh module")
		app.store.data.reduced_motion = true
		app.hint()
		check(app.play_button.has_focus(), "Hint focuses target")
		for i in range(3): app.play_button.pressed.emit()
		check(app.store.data.completed.get(entry.id, false), "Completion: " + entry.id)
		app.advance()
		check(app.taps == 3, "Completion is idempotent")
		app.open_module(foundation_entry)
		check(app.taps == 0, "Retry resets activity")
		app.hub()
		check(app.grid.get_child_count() == 5, "Return to hub")
	var saved = load("res://core/save_store.gd").new()
	saved.load_save()
	check(saved.data.completed.size() == 3, "Save round trip")
	app.size = Vector2(360, 800)
	app.responsive()
	check(app.grid.columns == 1, "Portrait layout")
	app.size = Vector2(1024, 600)
	app.responsive()
	check(app.grid.columns == 2, "Landscape layout")
	app.settings()
	app.confirm_reset()
	check(app.store.data.completed.size() == 3, "Reset requires confirmation")
	check(saved.reset() == OK, "Reset writes successfully")
	saved.load_save()
	check(saved.data.completed.is_empty(), "Reset persisted")
	var f = FileAccess.open(saved.PATH, FileAccess.WRITE)
	f.store_string("invalid JSON")
	f.close()
	saved.load_save()
	check(saved.data.schema == 1 and saved.data.completed.is_empty(), "Corrupt save recovers")
	f = FileAccess.open(saved.PATH, FileAccess.WRITE)
	f.store_string('{"schema":999}')
	f.close()
	saved.load_save()
	check(saved.data.schema == 1, "Unknown schema recovers")
	app.store.data.muted = true
	app.audio.stop()
	app.sound()
	check(not app.audio.playing, "Mute prevents playback")
	var back := InputEventAction.new()
	back.action = "ui_cancel"
	back.pressed = true
	app._unhandled_input(back)
	check(app.active.is_empty(), "Keyboard back returns to hub")
	app.audio.stop()
	await create_timer(0.5).timeout
	app.queue_free()
	await process_frame
	print("RESULT: %d checks, %d failures" % [checks, failures])
	quit(1 if failures else 0)
