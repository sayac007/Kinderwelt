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
		for look in ["hero","alien","astronaut","scientist"]:
			for b in game.hero_choices:b.get_child(0).costume=look
			game.arrange_chooser()
			await snap(profile.id+"-looks-"+look)
		for b in game.hero_choices:b.get_child(0).costume="classic"
		game.arrange_chooser()
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
		for id in ["george","squirrel"]:
			game.world.hero.person=id
			game.world.hero.costume="astronaut" if id=="george" else "scientist"
			game.world.hero.animation="move"
			await snap(profile.id+"-"+id+"-world")
			game.world.hero.react()
			await snap(profile.id+"-"+id+"-success")
		game.switch_subject("physics");game.open_task(19)
		app.simulated_dpi=420
		root.size=Vector2i(profile.size.y,profile.size.x);app.update_mobile()
		await snap(profile.id+"-rotated-live-task")
		root.size=profile.size;app.update_mobile()
		await snap(profile.id+"-restored-live-task")
		game.close_task()
		app.simulated_dpi=profile.dpi;app.update_mobile()
		for scene in preload("res://core/quest/scenery.gd").IDS:
			app.store.data.subject_sceneries[game.subject]=scene
			game.world.set_page(0)
			game.world.clock=0.2
			await snap(profile.id+"-scene-"+scene)
			if scene in ["castle","tree","seabed","city","moon"]:
				game.world.clock=4.2
				game.world.hero.animation=game.world.motion_mode(true)
				game.world.target_x=game.world.hero_x+80
				await snap(profile.id+"-scene-"+scene+"-floating")
			if scene=="tree":
				game.world.hero_x=game.world.arrival_distance(0);game.world.target_x=game.world.hero_x
				game.world.camera_x=game.world.follow_camera();game.world._process(0)
				await snap(profile.id+"-scene-tree-branch")
		app.store.data.subject_sceneries[game.subject]="auto"
		game.world.set_page(3)
		await snap(profile.id+"-last-trail")
		var previous_progress: Dictionary=app.store.data.quest.duplicate(true)
		for task in preload("res://games/quest/progress.gd").tasks():preload("res://games/quest/progress.gd").award(app.store.data.quest,task.id)
		app.store.data.hero="squirrel";game.world.hero.person="squirrel"
		game.update_score();game.arrange()
		await snap(profile.id+"-header-max-points")
		game.open_task(0)
		await snap(profile.id+"-header-max-points-task")
		game.close_task();app.store.data.quest=previous_progress
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
		app.sceneries()
		await snap(profile.id+"-scenery-picker")
		app.narration.cancel();app.audio.music.shutdown();app.audio.stop()
		await create_timer(.15).timeout
		app.free()
		await process_frame
		root.content_scale_size=Vector2i.ZERO
	# Large actual-engine galleries let reviewers inspect all 35 character/look combinations.
	root.size=Vector2i(1200,800);root.content_scale_size=Vector2i.ZERO
	for id in preload("res://core/quest/hero.gd").IDS:
		var gallery:=ColorRect.new();gallery.color=Color("19384f");gallery.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		root.add_child(gallery)
		var title:=Label.new();title.text=preload("res://core/quest/hero.gd").NAMES[id]
		title.position=Vector2(20,20);title.size=Vector2(1160,60);title.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
		title.add_theme_font_override("font",preload("res://core/quest/art.gd").font());title.add_theme_font_size_override("font_size",36);gallery.add_child(title)
		for index in range(5):
			var look: String=preload("res://core/quest/wardrobe.gd").LOOKS[index]
			var figure:=preload("res://core/quest/hero.gd").new();figure.person=id;figure.costume=look;figure.animation="move";figure.selected=true
			var height:=minf(570,210/figure.aspect());figure.size=Vector2(height*figure.aspect(),height)
			figure.position=Vector2(14+index*236+(224-figure.size.x)/2,110+(570-height)/2)
			gallery.add_child(figure)
			var caption:=Label.new();caption.text=preload("res://core/quest/language.gd").text("look_"+look,"de")
			caption.position=Vector2(14+index*236,710);caption.size=Vector2(224,45);caption.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
			caption.add_theme_font_override("font",preload("res://core/quest/art.gd").font());caption.add_theme_font_size_override("font_size",24);gallery.add_child(caption)
		await snap("gallery-"+id)
		gallery.free()
	FileAccess.open(output.path_join("renders.json"),FileAccess.WRITE).store_string(JSON.stringify(frames,"  "))
	print("QUEST RENDER: ",frames.size()," frames")
	await create_timer(.25).timeout
	quit()
