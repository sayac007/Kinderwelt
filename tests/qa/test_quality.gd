extends "res://addons/gut/test.gd"
const Catalog = preload("res://core/catalog.gd")
const Store = preload("res://core/save_store.gd")
const Scene = preload("res://core/main.tscn")
var policy: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://tests/qa/policy.json"))
var coverage: Array = []
var task_cases: Array = make_cases()

func should_skip_script():
	if not OS.get_environment("XDG_DATA_HOME").begins_with("/tmp/kinderwelt-quality."):
		return "Use tests/qa/run.sh: these tests require isolated synthetic save data."
	return false

func make_cases() -> Array:
	var result := []
	for entry in Catalog.modules():
		var levels := Catalog.levels(entry)
		for i in range(levels.size()):
			for dimensions in policy.viewports:
				result.append({"entry":entry,"index":i,"id":levels[i].id,"viewport":dimensions})
	return result

func before_each() -> void:
	# Guarded by should_skip_script; never touches a developer's actual saves.
	DirAccess.remove_absolute(ProjectSettings.globalize_path(Store.PATH))
	DirAccess.remove_absolute(ProjectSettings.globalize_path(Store.PATH+".tmp"))

func after_all() -> void:
	var path := OS.get_environment("KINDERWELT_QA_OUTPUT")
	if path.is_empty(): return
	var file := FileAccess.open(path.path_join("coverage.json"),FileAccess.WRITE)
	if file==null:
		push_error("Coverage report cannot be written")
		return
	file.store_string(JSON.stringify({"schema":1,"cases":coverage},"  "))

func app_instance() -> Control:
	var app := Scene.instantiate()
	get_tree().root.add_child(app)
	autofree(app)
	app.store.data.muted = true
	app.store.data.reduced_motion = true
	return app

func settle() -> void:
	await wait_process_frames(2)

func buttons(node: Node) -> Array:
	var result := []
	for child in node.get_children():
		if child is Button: result.append(child)
		result.append_array(buttons(child))
	return result

func cancel_replay(game: Control) -> void:
	game.cancel_demonstration()

func solve(game: Control) -> void:
	for _step in range(128):
		if game.model.complete(): return
		var move = game.model.next_hint()
		if move is Array:
			if move.is_empty(): break
			if move==[-1,-1]: game.undo_button.pressed.emit()
			elif game.levels[game.index].get("mode")=="compare": game.socket_buttons[move[0]].pressed.emit()
			else:
				game.source_buttons[move[0]].pressed.emit()
				game.socket_buttons[move[1]].pressed.emit()
		else:
			match move.get("action"):
				"place":
					game.source_buttons[move.source].pressed.emit()
					game.socket_buttons[move.target].pressed.emit()
				"set":
					for cycle in range(5):
						if int(game.model.values[move.control])==int(move.value): break
						game.source_buttons[move.control].pressed.emit()
				"test": game.socket_buttons[0].pressed.emit()
				"choose": game.source_buttons[move.choice].pressed.emit()
				"undo": game.undo_button.pressed.emit()
				_: break
	fail_test("No completion within the bounded move budget")

func assert_task_focus(game: Control) -> void:
	var focused := get_tree().root.gui_get_focus_owner()
	assert_true(is_instance_valid(focused) and game.is_ancestor_of(focused),"Keyboard focus remains inside the active game")

func test_inventory_and_framework_version() -> void:
	assert_eq(Engine.get_version_info().hash.left(9),policy.engine_version.get_slice(".",5),"Exact pinned engine build")
	var modules := Catalog.modules()
	assert_eq(modules.size(),policy.minimum_tasks.size())
	var seen := []
	for entry in modules:
		assert_false(entry.id in seen,"Registered module IDs are unique")
		seen.append(entry.id)
		var levels := Catalog.levels(entry)
		assert_gte(levels.size(),int(policy.minimum_tasks.get(entry.id,1)),"Every authored collection validates")
	assert_gt(task_cases.size(),0,"No empty or silently skipped matrix")

func test_every_task_at_every_viewport(case = use_parameters(task_cases)) -> void:
	var before: int = get_fail_count()
	var dimensions := Vector2i(int(case.viewport[0]),int(case.viewport[1]))
	get_tree().root.size = dimensions
	var app := app_instance()
	await settle()
	app.open_module(case.entry)
	await settle()
	assert_lte(app.body.size.x,float(dimensions.x)+1,"Chooser fits the viewport")
	var game: Control = app.learning_game
	for retry in range(int(policy.retries)):
		game.start_level(case.index)
		cancel_replay(game)
		assert_false(game.model.complete(),"Repeated retry starts an incomplete task")
		assert_true(game.model.history.is_empty(),"Repeated retry clears transient actions")
	await settle()
	assert_lte(app.body.size.x,float(dimensions.x)+1,"Task fits small phone/tablet")
	var controls := buttons(game)
	assert_gt(controls.size(),0,"Playable controls exist")
	for button in controls:
		assert_gte(button.size.x,float(policy.minimum_target[0]),"Wide tap target")
		assert_gte(button.size.y,float(policy.minimum_target[1]),"Tall tap target")
		assert_gte(button.get_global_rect().position.x,-1.0,"No left clipping")
		assert_lte(button.get_global_rect().end.x,float(dimensions.x)+1,"No right clipping")
		assert_false(button.tooltip_text.is_empty(),"Controls have supplemental German labels")
		assert_ne(button.focus_mode,Control.FOCUS_NONE,"Controls support keyboard focus")
	# Check real scroll geometry for both ends of each long task. No port/PID proxy.
	var scroll: ScrollContainer = app.body.get_parent()
	for button in [controls[0],controls[-1]]:
		scroll.ensure_control_visible(button)
		await settle()
		assert_true(get_tree().root.get_visible_rect().has_point(button.get_global_rect().get_center()),"Navigation/control can be scrolled into view")
	solve(game)
	assert_true(game.model.complete(),"Authored task completed through actual game controls")
	assert_true(game.recorded,"Completion is persisted")
	var restored := Store.new()
	restored.load_save()
	assert_true(restored.data.completed.get(case.entry.id,false),"Save/reload keeps module completion")
	assert_true(restored.data.learning[case.entry.id].completed.has(case.id),"Save/reload keeps exact task completion")
	game.undo_button.pressed.emit()
	assert_false(game.model.complete(),"Undo after success is reversible")
	assert_false(app.audio.playing,"Mute applies to the entire task")
	var back := InputEventAction.new()
	back.action="ui_cancel"
	back.pressed=true
	app._unhandled_input(back)
	assert_eq(app.grid.get_child_count(),5,"Back navigation reaches all five hub areas")
	coverage.append({"module":case.entry.id,"task":case.id,"viewport":case.viewport,"status":"PASS" if get_fail_count()==before else "FAIL","scope":"synthetic software checks; no child or device observations"})
	app.queue_free()
	await settle()

func test_keyboard_focus_after_entry_action_and_undo() -> void:
	for entry in Catalog.modules():
		var app := app_instance()
		await settle()
		app.open_module(entry)
		var game: Control = app.learning_game
		game.start_level(0)
		cancel_replay(game)
		await settle()
		assert_task_focus(game)
		game.source_buttons[0].pressed.emit()
		await settle()
		assert_task_focus(game)
		game.undo_button.pressed.emit()
		await settle()
		assert_task_focus(game)
		app.queue_free()
		await settle()

func test_fresh_install_write_failure_and_optional_save_recovery() -> void:
	var saved := Store.new()
	assert_false(FileAccess.file_exists(Store.PATH),"Fresh synthetic install has no previous save")
	saved.load_save()
	assert_eq(saved.data,Store.defaults(),"Fresh install uses safe defaults")
	saved.data.completed["logic"]=true
	assert_eq(saved.persist(),OK)
	var blocker := ProjectSettings.globalize_path(Store.PATH+".tmp")
	assert_eq(DirAccess.make_dir_absolute(blocker),OK)
	saved.data.completed["math"]=true
	assert_ne(saved.persist(),OK,"A failed atomic write is reported")
	var reload := Store.new()
	reload.load_save()
	assert_true(reload.data.completed.get("logic",false),"Write failure preserves the previous valid save")
	assert_false(reload.data.completed.get("math",false))
	assert_eq(DirAccess.remove_absolute(blocker),OK)
	var progress = preload("res://core/learning_progress.gd")
	for malformed in [null,[],{"math":null},{"math":{"tier":1,"completed":{},"recent":"invalid"}}]:
		reload.data.learning=malformed
		assert_eq(progress.state(reload,"math").tier,1,"Malformed optional fields recover safely")

func test_animated_hint_cancellation_and_system_back_for_all_areas() -> void:
	for entry in Catalog.modules():
		var app := app_instance()
		await settle()
		app.store.data.reduced_motion=false
		app.open_module(entry)
		var game: Control = app.learning_game
		var last: int = game.levels.size()-1
		game.start_level(last)
		cancel_replay(game)
		game.hint()
		game.hint()
		game.hint()
		game.start_level(0)
		cancel_replay(game)
		await wait_seconds(0.7)
		assert_eq(game.index,0,"Old asynchronous example cannot change a retried task")
		assert_true(game.model.history.is_empty(),"Old callbacks cannot modify new task history")
		app._notification(Node.NOTIFICATION_WM_GO_BACK_REQUEST)
		assert_eq(app.grid.get_child_count(),5,"System-back handler reaches hub")
		app.queue_free()
		await settle()

func test_entry_keeps_navigation_visible_on_small_phone() -> void:
	get_tree().root.size=Vector2i(320,568)
	for entry in Catalog.modules():
		var app := app_instance()
		await settle()
		app.open_module(entry)
		var game: Control = app.learning_game
		await settle()
		app.body.get_parent().scroll_vertical=int(app.body.size.y)
		await settle()
		game.start_level(game.levels.size()-1)
		cancel_replay(game)
		await settle()
		var home: Button = buttons(game)[0]
		assert_eq(get_tree().root.gui_get_focus_owner(),home,"Start focus anchors the top instruction/navigation area")
		assert_true(get_tree().root.get_visible_rect().has_point(home.get_global_rect().get_center()),"Task entry keeps navigation visible before any child action: "+entry.id)
		app.queue_free()
		await settle()
