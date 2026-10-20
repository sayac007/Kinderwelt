extends SceneTree
var output := ""
var frames := []
func _initialize() -> void:
	output = OS.get_environment("KINDERWELT_RENDER_OUTPUT")
	call_deferred("run")
func snap(name: String) -> void:
	for i in range(4): await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_texture().get_image()
	if img.save_png(output.path_join(name+".png"))!=OK: push_error("Cannot save render");quit(1)
	frames.append({"name":name,"pixels":[img.get_width(),img.get_height()]})
func run() -> void:
	if output.is_empty() or DisplayServer.get_name()=="headless": push_error("A real graphics backend is required");quit(1);return
	for profile in [{"id":"phone","size":Vector2i(360,800),"dpi":0},{"id":"small","size":Vector2i(320,568),"dpi":0},{"id":"landscape","size":Vector2i(800,360),"dpi":0},{"id":"dense","size":Vector2i(1080,2400),"dpi":420}]:
		root.size = profile.size
		var app: Control = load("res://core/quest/main.tscn").instantiate()
		app.simulated_dpi = profile.dpi
		root.add_child(app)
		app.store.reset()
		app.store.data.muted = true
		app.audio.sync_settings()
		app.hub()
		var game: Control = app.game_view
		await snap(profile.id+"-heroes")
		for pose in ["move","think","success"]:
			for b in game.hero_choices:
				b.get_child(0).reaction=0
				b.get_child(0).animation=pose
				b.get_child(0).clock=.21
			await snap(profile.id+"-heroes-"+pose)
		game.finish_hero()
		for subject in preload("res://games/quest/progress.gd").SUBJECTS:
			game.switch_subject(subject)
			await snap(profile.id+"-"+subject+"-world")
			for index in (range(8) if subject in ["math","german","logic"] else [0,19,39]):
				game.open_task(index)
				await snap(profile.id+"-"+subject+"-task-"+str(index))
				if index==0:
					game.task_panel.answer(game.task_panel.task.answer)
					await snap(profile.id+"-"+subject+"-solved")
				game.close_task()
		game.world.set_page(3)
		await snap(profile.id+"-last-trail")
		for locale in ["en","ru"]:
			app.store.data.locale=locale;app.hub();game=app.game_view
			game.switch_subject("physics");game.open_task(19)
			await snap(profile.id+"-"+locale+"-physics")
			game.close_task();game.switch_subject("german");game.open_task(20)
			await snap(profile.id+"-"+locale+"-german")
			app.languages();await snap(profile.id+"-"+locale+"-languages")
		app.store.data.locale="de"
		app.musicbox()
		await snap(profile.id+"-musicbox")
		app.settings()
		await snap(profile.id+"-settings")
		app.narration.cancel();app.audio.music.shutdown();app.audio.stop()
		await create_timer(.15).timeout
		app.free()
		await process_frame
		root.content_scale_size=Vector2i.ZERO
	FileAccess.open(output.path_join("renders.json"),FileAccess.WRITE).store_string(JSON.stringify(frames,"  "))
	print("QUEST RENDER: ",frames.size()," frames")
	await create_timer(.25).timeout
	quit()
