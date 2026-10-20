extends SceneTree
var frames := []
var output := ""
func _initialize() -> void:
	output = OS.get_environment("KINDERWELT_RENDER_OUTPUT")
	call_deferred("capture")
func snap(name: String,profile: Dictionary) -> void:
	for i in range(3): await process_frame
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	var file: String = profile.name+"_"+name+".png"
	if image.save_png(output.path_join(file))!=OK: push_error("Render save failed");quit(1)
	frames.append({"file":file,"state":name,"pixels":[image.get_width(),image.get_height()]})
func capture() -> void:
	if output.is_empty() or DisplayServer.get_name()=="headless": push_error("Real display/output required");quit(1);return
	for profile in [{"name":"small","size":Vector2i(320,568),"dpi":0},{"name":"large-text","size":Vector2i(320,568),"dpi":0,"text_scale":1.15},{"name":"phone","size":Vector2i(360,800),"dpi":0},{"name":"landscape","size":Vector2i(800,360),"dpi":0},{"name":"dense","size":Vector2i(1080,2400),"dpi":420}]:
		root.size = profile.size
		var app: Control = load("res://core/main.tscn").instantiate()
		app.simulated_dpi = profile.dpi
		root.add_child(app)
		app.store.reset()
		app.store.data.text_scale = profile.get("text_scale",1.0)
		app.store.data.muted = true
		app.store.data.reduced_motion = true
		app.audio.sync_settings()
		app.sound_button.text = "Ton an"
		app.hub()
		await snap("map",profile)
		app.scroll_view.scroll_vertical = 560
		await snap("map-bottom",profile)
		app.heroes()
		app.scroll_view.scroll_vertical = 0
		await snap("heroes",profile)
		for pose in ["idle","move","think","success"]:
			for button in app.body.get_child(2).get_children():
				button.get_child(0).animation = pose
				button.get_child(0).reduced_motion = false
				button.get_child(0).clock = .2
			await snap("heroes-"+pose,profile)
		app.musicbox()
		app.scroll_view.scroll_vertical = 0
		await snap("musicbox",profile)
		for tier in range(3):
			app.hub()
			app.store.data.water_tier = tier
			app.store.data.hero = ["mina","leo","sam"][tier]
			app.open_water()
			var game: Control = app.modern_view
			await snap("water-"+str(tier),profile)
			var targets: Dictionary = [{5:10,6:10},{5:10,6:14,10:5},{5:10,6:13,2:6,10:5,14:3}][tier]
			for key in targets:
				for i in range(4):
					if game.model.tiles[key]==targets[key]: break
					game.model.rotate(key)
			game.turn_water()
			await create_timer(.7).timeout
			await snap("water-solved-"+str(tier),profile)
		app.free()
		await process_frame
		root.content_scale_size = Vector2i.ZERO
	var file := FileAccess.open(output.path_join("modern-render.json"),FileAccess.WRITE)
	file.store_string(JSON.stringify({"scope":"Real desktop software rendering, simulated DPI; not Android hardware","frames":frames},"  "))
	file.close()
	print("MODERN RENDER: %d frames" % frames.size())
	await create_timer(.3).timeout
	quit()
