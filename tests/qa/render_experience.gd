extends SceneTree
const Catalog = preload("res://core/catalog.gd")
const Mobile = preload("res://core/mobile.gd")
var frames := []
var output := ""

func _initialize() -> void:
	output = OS.get_environment("KINDERWELT_RENDER_OUTPUT")
	call_deferred("capture")

func snapshot(app: Control,name: String,profile: Dictionary) -> void:
	await process_frame
	await process_frame
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	var file := "%s_%s.png" % [profile.name,name]
	if image.save_png(output.path_join(file))!=OK:
		push_error("Could not save experience screenshot")
		quit(1)
	frames.append({"file":file,"pixels":[image.get_width(),image.get_height()],"logical_size":[app.size.x,app.size.y],"dpi_simulation":profile.dpi,"state":name})

func capture() -> void:
	if output.is_empty() or DisplayServer.get_name()=="headless":
		push_error("A rendering display and KINDERWELT_RENDER_OUTPUT are required")
		quit(1)
		return
	var profiles := [
		{"name":"small-phone","size":Vector2i(320,568),"dpi":160},
		{"name":"phone","size":Vector2i(360,800),"dpi":160},
		{"name":"tablet","size":Vector2i(768,1024),"dpi":160},
		{"name":"dense-phone","size":Vector2i(1080,2400),"dpi":420}]
	for profile in profiles:
		root.size=profile.size
		var app: Control = load("res://core/main.tscn").instantiate()
		app.simulated_dpi = profile.dpi if profile.dpi>160 else 0.0
		root.add_child(app)
		app.store.data.muted=true
		app.store.data.reduced_motion=true
		app.audio.sync_settings()
		await process_frame
		await process_frame
		app.hub()
		app.body.get_parent().follow_focus=false
		await snapshot(app,"hub",profile)
		for entry in Catalog.modules():
			app.open_module(entry)
			var game: Control=app.learning_game
			game.start_level(2 if entry.id=="autonomy" else 0)
			game.cancel_demonstration()
			app.body.get_parent().scroll_vertical=0
			await snapshot(app,entry.id+"-start",profile)
			game.hint();game.hint();game.hint()
			game.cancel_demonstration()
			await process_frame
			if not game.model.complete():
				push_error("Representative task did not complete")
				quit(1)
				return
			app.body.get_parent().scroll_vertical=int(app.body.size.y)
			await snapshot(app,entry.id+"-complete",profile)
		app.queue_free()
		await process_frame
		root.content_scale_size=Vector2i.ZERO
	var report := FileAccess.open(output.path_join("experience-render.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify({"scope":"Real desktop software-rendered UI, including simulated density; no Android device or child observation","frames":frames},"  "))
	report.close()
	print("EXPERIENCE RENDER: %d frames" % frames.size())
	quit()
