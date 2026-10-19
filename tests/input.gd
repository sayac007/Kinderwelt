extends SceneTree
const Catalog = preload("res://core/catalog.gd")
var checks := 0
var failures := 0

func check(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		failures += 1
		push_error(message)

func _initialize() -> void:
	call_deferred("run")

# Actual GUI event dispatch, without invoking the pressed signal ourselves.
# Synthetic touch is a smoke test, not a physical touchscreen check.
func touch(button: Button) -> void:
	var parent: Node = button.get_parent()
	while parent != null and not parent is ScrollContainer:
		parent = parent.get_parent()
	if parent is ScrollContainer:
		parent.ensure_control_visible(button)
	await process_frame
	await process_frame
	var point: Vector2 = root.get_final_transform() * button.get_global_rect().get_center()
	var down := InputEventScreenTouch.new()
	down.index = 0
	down.position = point
	down.pressed = true
	Input.parse_input_event(down)
	await process_frame
	var up := InputEventScreenTouch.new()
	up.index = 0
	up.position = point
	up.pressed = false
	Input.parse_input_event(up)
	await process_frame
	await process_frame

func run() -> void:
	root.size = Vector2i(900,700)
	var app = load("res://core/main.tscn").instantiate()
	root.add_child(app)
	await process_frame
	app.store.data.muted = true
	app.store.data.reduced_motion = true
	var entries := Catalog.modules()
	for entry in entries.slice(0,2):
		app.open_module(entry)
		var game = app.learning_game
		game.start_level(0)
		await process_frame
		await touch(game.source_buttons[0])
		check(game.selected==0,entry.id+" synthetic touch selects item")
		await touch(game.socket_buttons[0])
		check(game.model.placements[0]==0,entry.id+" synthetic touch places item")
		# Keyboard activation of the focused undo control through GUI dispatch.
		game.undo_button.grab_focus()
		var key := InputEventKey.new()
		key.keycode = KEY_ENTER
		key.pressed = true
		root.push_input(key,true)
		key = InputEventKey.new()
		key.keycode = KEY_ENTER
		key.pressed = false
		root.push_input(key,true)
		await process_frame
		check(game.model.history.is_empty(),entry.id+" keyboard undo")
		for viewport_size in [Vector2i(360,800),Vector2i(1024,600)]:
			root.size = viewport_size
			await process_frame
			await process_frame
			check(root.get_visible_rect().size==Vector2(viewport_size),"Viewport uses actual window size")
			check(app.get_minimum_size().x <= root.get_visible_rect().size.x,"Minimum width fits viewport")
			check(game.size.x <= root.get_visible_rect().size.x+1,"Game fits viewport width")
			for b in game.source_buttons:
				check(b.size.x>=96 and b.size.y>=72,"Large item hit target")
			check(game.layout_grids[0].columns==(3 if app.size.x<600 else 5),"Responsive inventory columns")
			await touch(game.source_buttons[0])
			check(game.selected==0,"Touch selects after rotation")
			await touch(game.socket_buttons[0])
			check(game.model.placements[0]==0,"Touch places after rotation")
			game.undo()
		app.hub()
		await process_frame
	# Wrong comparisons explain the mismatch without consuming a chance.
	app.open_module(entries[1])
	var comparison = app.learning_game
	comparison.start_level(1)
	await touch(comparison.socket_buttons[0])
	check(not comparison.model.complete() and comparison.rejected==0,"Wrong comparison remains retryable")
	await touch(comparison.socket_buttons[1])
	check(comparison.model.complete(),"Comparison can be corrected by touch")
	app.hub()
	# Animated worked example must remain interruptible, including retry/home.
	app.open_module(entries[0])
	var game = app.learning_game
	app.store.data.reduced_motion = false
	game.start_level(8)
	game.hint()
	game.hint()
	game.hint() # starts asynchronous demonstration
	check(game.demonstrating,"Worked example animates step by step")
	game.start_level(0)
	await create_timer(0.6).timeout
	check(game.index==0 and game.model.history.is_empty(),"Retry cancels stale demonstration")
	game.hint()
	game.hint()
	game.hint()
	app.hub()
	await create_timer(0.6).timeout
	check(app.grid.get_child_count()==5,"Home cancels demonstration without soft lock")
	app.audio.stop()
	app.queue_free()
	await process_frame
	print("INPUT RESULT: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
