extends SceneTree
const Avatar=preload("res://core/quest/custom_avatar.gd")
var output: String
var captures: Array=[]
func _initialize() -> void:call_deferred("run")
func snap(file: String,locale: String,view: String) -> void:
	for frame in range(6):await process_frame
	await RenderingServer.frame_post_draw
	var image:=root.get_texture().get_image()
	if image.save_png(output.path_join(file))!=OK:push_error("Store capture failed");quit(1);return
	captures.append({"file":file,"locale":locale,"view":view,"width":image.get_width(),"height":image.get_height()})
func run() -> void:
	output=OS.get_environment("KINDERWELT_STORE_OUTPUT")
	if output.is_empty() or DisplayServer.get_name()=="headless":push_error("Store capture needs a graphics backend and isolated output");quit(1);return
	if JSON.parse_string(FileAccess.get_file_as_string("res://assets/quest/cast.json")).variant!="public":push_error("Store capture requires the neutral cast");quit(1);return
	seed(1)
	var icon:=Image.new()
	if icon.load_png_from_buffer(FileAccess.get_file_as_bytes("res://assets/quest/appicon.png"))!=OK:quit(1);return
	icon.resize(512,512,Image.INTERPOLATE_LANCZOS)
	if icon.save_png(output.path_join("icon-512.png"))!=OK:quit(1);return
	captures.append({"file":"icon-512.png","locale":"","view":"icon","width":512,"height":512})
	root.size=Vector2i(1024,500);root.content_scale_size=Vector2i.ZERO
	var feature: Control=load("res://store/feature.gd").new();feature.size=Vector2(1024,500);root.add_child(feature)
	await snap("feature-1024x500.png","","feature");feature.free()
	var silhouette:=Image.new()
	if silhouette.load_svg_from_string(FileAccess.get_file_as_string("res://store/silhouette.svg"))!=OK:quit(1);return
	if silhouette.save_png("user://store-silhouette.png")!=OK:quit(1);return
	for locale in ["de","en","ru"]:
		root.size=Vector2i(1080,1920);root.content_scale_size=Vector2i.ZERO
		var app: Control=load("res://core/quest/main.tscn").instantiate();app.simulated_dpi=420;root.add_child(app)
		app.store.reset();app.store.data.locale=locale;app.store.data.muted=true;app.store.data.voice_auto=false;app.store.data.reduced_motion=true
		app.audio.sync_settings();app.hub()
		await snap(locale+"-01-characters.png",locale,"characters")
		app.parents();app.manage_avatar()
		await app.avatar_manager.load_path("user://store-silhouette.png")
		app.avatar_manager.preview.set_portrait(true)
		app.avatar_manager.scroll.scroll_vertical=maxi(0,roundi(app.avatar_manager.preview.position.y-30))
		await snap(locale+"-02-own-character.png",locale,"own-character-synthetic")
		app.avatar_manager.confirm_button.pressed.emit()
		var game: Control=app.game_view
		game.switch_subject("math")
		await snap(locale+"-03-world.png",locale,"world")
		game.open_task(0)
		await snap(locale+"-04-maths.png",locale,"maths")
		game.task_panel.answer(game.task_panel.task.answer)
		await snap(locale+"-05-reward.png",locale,"reward")
		app.narration.cancel();app.audio.music.shutdown();app.audio.stop();app.free()
		for frame in range(3):await process_frame
	Avatar.erase();DirAccess.remove_absolute("user://store-silhouette.png")
	var report:=FileAccess.open(output.path_join("captures.json"),FileAccess.WRITE)
	report.store_string(JSON.stringify(captures,"\t"));report.close()
	print("STORE RENDER: ",captures.size()," images; neutral only, synthetic silhouette, no real photos")
	quit(0)
