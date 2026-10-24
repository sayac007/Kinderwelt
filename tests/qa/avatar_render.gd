extends SceneTree
const Avatar=preload("res://core/quest/custom_avatar.gd")
const Store=preload("res://core/save_store.gd")
var output := ""
var captures := 0
func _initialize() -> void:call_deferred("run")
func snap(name: String) -> void:
	for frame in range(4):await process_frame
	await RenderingServer.frame_post_draw
	if root.get_texture().get_image().save_png(output.path_join(name+".png"))!=OK:
		push_error("Could not save avatar UI render");quit(1)
	captures+=1
func run() -> void:
	output=OS.get_environment("KINDERWELT_AVATAR_RENDER_OUTPUT")
	if output.is_empty() or DisplayServer.get_name()=="headless":
		push_error("Pass an isolated render output and a graphics backend");quit(1);return
	DirAccess.make_dir_recursive_absolute(output)
	var source:=FileAccess.get_file_as_bytes("res://tests/fixtures/avatar/gps-source.png")
	for locale in ["de","en","ru"]:
		for profile in [{"id":"phone","size":Vector2i(360,800)},{"id":"landscape","size":Vector2i(800,360)}]:
			root.size=profile.size
			var stored:=Store.new();stored.data.locale=locale;stored.data.muted=true;stored.data.voice_auto=false
			stored.data.quest.hero_chosen=true;stored.data.hero="custom"
			Avatar.store(Avatar.prepare(source).image);stored.persist()
			var app: Control=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
			for frame in range(5):await process_frame
			# Only synthetic imported pixels are visible; do not capture the family chooser.
			app.parents();app.manage_avatar()
			var panel: Control=app.avatar_manager
			await snap(locale+"-"+profile.id+"-help")
			panel.candidate=Avatar.prepare(source).image
			panel.preview.texture=ImageTexture.create_from_image(panel.candidate)
			panel.preview.queue_redraw();panel.help_text.hide();panel.confirm_button.disabled=false
			await snap(locale+"-"+profile.id+"-preview")
			await panel.load_path("res://tests/fixtures/avatar/orientation-1.jpg")
			panel.preview.set_zoom(1.8);panel.preview.pan(Vector2(12,0))
			panel.scroll.scroll_vertical=maxi(0,roundi(panel.preview.position.y-20))
			await snap(locale+"-"+profile.id+"-crop")
			panel.confirm_button.pressed.emit()
			await snap(locale+"-"+profile.id+"-world")
			app.audio.music.shutdown();app.narration.cancel();app.queue_free()
			for frame in range(3):await process_frame
	Avatar.erase()
	print("AVATAR RENDER: ",captures," real frames; synthetic local image; three locales, two orientations")
	quit(0)
