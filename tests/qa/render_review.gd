extends SceneTree
const Catalog = preload("res://core/catalog.gd")
var frames := []

func _initialize() -> void:
	call_deferred("capture")

func capture() -> void:
	var output := OS.get_environment("KINDERWELT_RENDER_OUTPUT")
	if output.is_empty() or DisplayServer.get_name()=="headless":
		push_error("Use tests/qa/render.sh with an actual rendering backend")
		quit(1)
		return
	var app = load("res://core/main.tscn").instantiate()
	root.add_child(app)
	await process_frame
	# Controlled review pages must not be repositioned by focus-following.
	app.body.get_parent().follow_focus=false
	app.store.data.muted=true
	app.store.data.reduced_motion=true
	for dimensions in [Vector2i(320,568),Vector2i(768,1024)]:
		root.size=dimensions
		for entry in Catalog.modules():
			app.open_module(entry)
			var game: Control = app.learning_game
			for i in range(game.levels.size()):
				game.start_level(i)
				game.cancel_demonstration()
				await process_frame
				await process_frame
				# The ScrollBar range is the effective laid-out range; VBox size can
				# still reflect an earlier chooser while its minimum is changing.
				await process_frame
				await RenderingServer.frame_post_draw
				var scroll: ScrollContainer = app.body.get_parent()
				var bar := scroll.get_v_scroll_bar()
				var last := maxi(0,int(ceil(bar.max_value-bar.page)))
				var positions := []
				for y in range(0,last+1,maxi(1,dimensions.y-40)): positions.append(y)
				if positions[-1]!=last: positions.append(last)
				var captured_positions := []
				for page in range(positions.size()):
					app.body.get_parent().scroll_vertical=positions[page]
					await process_frame
					await process_frame
					await RenderingServer.frame_post_draw
					var actual_y: int = scroll.scroll_vertical
					if actual_y in captured_positions: continue
					captured_positions.append(actual_y)
					var filename := "%s_%02d_%dx%d_p%02d.png" % [entry.id,i,dimensions.x,dimensions.y,page]
					var result := root.get_texture().get_image().save_png(output.path_join(filename))
					if result!=OK:
						push_error("Could not save synthetic QA render")
						quit(1)
						return
					frames.append({"module":entry.id,"task":game.levels[i].id,"viewport":[dimensions.x,dimensions.y],"page":page,"scroll_y":app.body.get_parent().scroll_vertical,"file":filename})
	var file := FileAccess.open(output.path_join("render.json"),FileAccess.WRITE)
	if file==null:
		push_error("Could not write render evidence")
		quit(1)
		return
	file.store_string(JSON.stringify({"schema":1,"backend":DisplayServer.get_name(),"scope":"synthetic initial UI; not a real device benchmark or child observation","frames":frames},"  "))
	file.close()
	app.queue_free()
	await create_timer(1.0).timeout
	print("RENDER REVIEW: %d frames" % frames.size())
	quit()
