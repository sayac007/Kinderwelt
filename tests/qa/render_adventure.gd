extends SceneTree
var frames := []
var output := ""
var failures := 0
func _initialize() -> void:
	output = OS.get_environment("KINDERWELT_RENDER_OUTPUT")
	call_deferred("capture")
func snapshot(app: Control,name: String,profile: Dictionary) -> void:
	for i in range(3): await process_frame
	await RenderingServer.frame_post_draw
	var file := "%s_%s.png" % [profile.name,name]
	var image := root.get_texture().get_image()
	if image.save_png(output.path_join(file))!=OK:
		push_error("Screenshot failed")
		failures += 1
	var game: Control = app.adventure
	var scroll_needed := false
	if is_instance_valid(game.overlay):
		var scroll: ScrollContainer = game.overlay.get_child(0)
		scroll_needed = scroll.get_v_scroll_bar().visible
	frames.append({"file":file,"pixels":[image.get_width(),image.get_height()],"state":name,"menu_scroll":scroll_needed,"world_size":[game.world.size.x,game.world.size.y]})
	for control in game.find_children("*","Button",true,false):
		if control.is_visible_in_tree() and (control.size.x<96 or control.size.y<72):
			push_error("Small touch control: "+control.text)
			failures += 1
func capture() -> void:
	if output.is_empty() or DisplayServer.get_name()=="headless":
		push_error("Real rendering backend and output required")
		quit(1)
		return
	for profile in [{"name":"small-phone","size":Vector2i(320,568),"dpi":0},{"name":"phone","size":Vector2i(360,800),"dpi":0},{"name":"landscape","size":Vector2i(800,360),"dpi":0},{"name":"dense-phone","size":Vector2i(1080,2400),"dpi":420}]:
		root.size = profile.size
		var app: Control = load("res://core/main.tscn").instantiate()
		app.simulated_dpi = profile.dpi
		root.add_child(app)
		app.store.reset()
		app.store.data.muted = true
		app.store.data.reduced_motion = true
		app.open_adventure()
		await snapshot(app,"intro",profile)
		var game: Control = app.adventure
		game.progress.introduced = true
		game.close_dialog()
		await snapshot(app,"workshop",profile)
		game.interact("right")
		game.world.controller.position = Vector2(460,365)
		game.world.controller.target = game.world.controller.position
		await snapshot(app,"power-room",profile)
		game.panel("sources")
		await snapshot(app,"sources",profile)
		for key in ["sun","wind","battery"]: game.change(key)
		game.diagnosis("sources")
		await snapshot(app,"protection",profile)
		game.change("wind")
		game.change("relay")
		game.change("door")
		game.panel("circuits")
		await snapshot(app,"solution",profile)
		game.close_dialog()
		game.world.controller.position = Vector2(750,365)
		game.world.controller.target = game.world.controller.position
		await snapshot(app,"open-gate",profile)
		game.interact("right")
		game.world.controller.position = Vector2(430,365)
		game.world.controller.target = game.world.controller.position
		await snapshot(app,"observatory",profile)
		game.pause_menu()
		await snapshot(app,"pause",profile)
		app.free()
		await process_frame
		root.content_scale_size = Vector2i.ZERO
	var report := FileAccess.open(output.path_join("adventure-render.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"scope":"Desktop software rendering, simulated Android density; no hardware test","frames":frames,"failures":failures},"  "))
	report.close()
	print("ADVENTURE RENDER: %d frames, %d failures" % [frames.size(),failures])
	quit(1 if failures else 0)
