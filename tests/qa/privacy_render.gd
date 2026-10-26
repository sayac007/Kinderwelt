extends SceneTree
var output: String
var captures:=0
func _initialize() -> void:call_deferred("run")
func snap(name: String) -> void:
	for frame in range(5):await process_frame
	await RenderingServer.frame_post_draw
	if root.get_texture().get_image().save_png(output.path_join(name+".png"))!=OK:push_error("Policy capture failed");quit(1)
	captures+=1
func run() -> void:
	output=OS.get_environment("KINDERWELT_PRIVACY_RENDER_OUTPUT")
	if output.is_empty() or DisplayServer.get_name()=="headless":push_error("Use isolated graphics QA wrapper");quit(1);return
	DirAccess.make_dir_recursive_absolute(output)
	for locale in ["de","en","ru"]:
		for profile in [{"id":"phone","size":Vector2i(360,800)},{"id":"landscape","size":Vector2i(800,360)}]:
			root.size=profile.size;root.content_scale_size=Vector2i.ZERO
			var app: Control=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
			app.store.reset();app.store.data.locale=locale;app.store.data.muted=true;app.store.data.voice_auto=false
			app.parents();app.privacy_policy()
			await snap(locale+"-"+profile.id+"-start")
			app.scroll_view.scroll_vertical=1000000
			await snap(locale+"-"+profile.id+"-end")
			app.narration.cancel();app.audio.music.shutdown();app.free()
			for frame in range(3):await process_frame
	print("PRIVACY RENDER: ",captures," real frames; three locales, two orientations; offline text")
	quit(0)
