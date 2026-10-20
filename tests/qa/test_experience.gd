extends "res://addons/gut/test.gd"
const Scene = preload("res://core/main.tscn")
const Catalog = preload("res://core/catalog.gd")
const Store = preload("res://core/save_store.gd")
const Design = preload("res://core/design.gd")
const Mobile = preload("res://core/mobile.gd")
var cases: Array = make_cases()

func should_skip_script():
	return false if OS.get_environment("XDG_DATA_HOME").begins_with("/tmp/kinderwelt-quality.") else "Use tests/qa/run.sh"

func make_cases() -> Array:
	var result := []
	for entry in Catalog.modules():
		for i in range(Catalog.levels(entry).size()):
			for dimensions in [Vector2i(320,568),Vector2i(360,800),Vector2i(768,1024),Vector2i(1024,768)]:
				result.append({"entry":entry,"index":i,"dimensions":dimensions})
	return result

func before_each() -> void:
	DirAccess.remove_absolute(ProjectSettings.globalize_path(Store.PATH))

func app_instance() -> Control:
	var app := Scene.instantiate()
	get_tree().root.add_child(app)
	autofree(app)
	app.store.data.muted = true
	app.audio.sync_settings()
	app.store.data.reduced_motion = true
	return app

func inspect(node: Node) -> void:
	if node is Label and not node.text.is_empty():
		assert_gte(node.get_theme_font_size("font_size"),18,"Readable text token: "+node.text)
		assert_lte(node.get_line_count(),node.get_visible_line_count(),"No cropped label: "+node.text)
		assert_gte(Design.contrast(node.get_theme_color("font_color"),Design.SURFACE),4.5,"Label contrast")
	if node is Button:
		assert_gte(node.size.x,96.0,"Touch width")
		assert_gte(node.size.y,72.0,"Touch height")
		assert_false(node.tooltip_text.is_empty(),"Named action")
	if node is Container:
		var controls := []
		for child in node.get_children():
			if child is Control and child.visible: controls.append(child)
		for i in range(controls.size()):
			for j in range(i+1,controls.size()):
				assert_false(controls[i].get_global_rect().intersects(controls[j].get_global_rect()),"Container siblings do not overlap")
	for child in node.get_children(): inspect(child)

func test_every_task_has_readable_unclipped_layout(case=use_parameters(cases)) -> void:
	get_tree().root.size=case.dimensions
	var app := app_instance()
	app.open_module(case.entry)
	var game: Control = app.learning_game
	game.start_level(case.index)
	game.cancel_demonstration()
	await wait_process_frames(3)
	inspect(app)
	assert_lte(app.top_bar.get_global_rect().end.y,app.scroll_view.get_global_rect().position.y,"Header and game do not overlap")
	assert_lte(app.body.size.x,float(case.dimensions.x),"No horizontal overflow")
	assert_true(app.sound_button.get_global_rect().get_center().y<80,"Mute always visible")
	if case.entry.id in ["language","autonomy","social"]:
		assert_false(is_instance_valid(game.adult_button),"No parent strip in child mode")
	app.queue_free()
	await wait_process_frames(1)

func test_density_and_palette_contract() -> void:
	for pixels in [Vector2i(1080,2400),Vector2i(2400,1080),Vector2i(1600,2560)]:
		for dpi in [240.0,420.0,480.0]:
			var logical := Mobile.logical_size(pixels,dpi)
			var scale := Vector2(pixels)/Vector2(logical)
			assert_gte(72.0*scale.y/dpi*160,48.0,"Density-mapped target at least 48 dp")
	assert_lte(Mobile.logical_size(Vector2i(1080,2400),0).x,420,"Unknown DPI falls back to readable phone scale")
	assert_gte(Design.contrast(Design.INK,Design.BACKGROUND),4.5)
	assert_gte(Design.contrast(Design.BORDER,Design.SURFACE),3.0)
	for color in Design.ACCENTS.values(): assert_gte(Design.contrast(Color(color),Design.SURFACE),4.5)
	var theme := Design.make_theme()
	for state in ["normal","hover","pressed","disabled"]:
		var background: Color = theme.get_stylebox(state,"Button").bg_color
		assert_gte(Design.contrast(Design.INK,background),4.5,"Text contrast in every button state")
	var font := ThemeDB.fallback_font
	for letter in "ÄÖÜäöüß": assert_true(font.has_char(letter.unicode_at(0)),"German glyph")

func test_audio_controls_playback_mute_and_persistence() -> void:
	var app := app_instance()
	app.store.data.muted=false
	app.audio.sync_settings()
	for entry in Catalog.modules():
		app.audio.set_world(entry.id)
		await wait_process_frames(2)
		var music: Node = app.audio.music
		var stream: AudioStreamWAV = music.players[music.active].stream
		assert_not_null(stream,"Real offline music for "+entry.id)
		assert_gt(stream.get_length(),15.0,"A full musical miniature exists")
		assert_eq(stream.loop_end,roundi(stream.get_length()*stream.mix_rate),"Loop covers entire decoded track")
		assert_true(music.players[music.active].playing,"Playback started")
	app.audio.music._notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	assert_true(app.audio.music.players[app.audio.music.active].stream_paused,"Background pause")
	app.audio.music._notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	assert_false(app.audio.music.players[app.audio.music.active].stream_paused,"Resume")
	app.settings()
	var sliders := []
	for child in app.body.get_children():
		if child is HSlider: sliders.append(child)
	assert_eq(sliders.size(),2,"Separate music and effect sliders")
	sliders[0].value=0.2
	sliders[1].value=0.0
	app.sound(true)
	assert_false(app.audio.playing,"Effects zero is silent")
	var loaded := Store.new()
	loaded.load_save()
	assert_almost_eq(float(loaded.data.music_volume),0.2,0.001)
	assert_almost_eq(float(loaded.data.effects_volume),0.0,0.001)
	app.sound_button.pressed.emit()
	assert_true(app.store.data.muted,"Global mute")
	for player in app.audio.music.players: assert_false(player.playing,"Mute stops all music voices")
	loaded.load_save()
	assert_true(loaded.data.muted,"Mute persisted")
	app.sound_button.pressed.emit()
	assert_true(app.audio.music.players[app.audio.music.active].playing,"Unmute resumes music")
	app.store.data.muted=true
	app.audio.sync_settings()

func test_legacy_save_and_malformed_audio_recovery() -> void:
	var legacy := {"schema":1,"completed":{"logic":true},"muted":false,"reduced_motion":true}
	var file := FileAccess.open(Store.PATH,FileAccess.WRITE)
	file.store_string(JSON.stringify(legacy));file.close()
	var saved := Store.new();saved.load_save()
	assert_true(saved.data.completed.logic,"Old progress survives")
	assert_almost_eq(float(saved.data.music_volume),0.35,0.001)
	legacy.music_volume="loud";legacy.effects_volume=-1
	file=FileAccess.open(Store.PATH,FileAccess.WRITE);file.store_string(JSON.stringify(legacy));file.close()
	saved.load_save()
	assert_almost_eq(float(saved.data.music_volume),0.35,0.001)
	assert_eq(float(saved.data.effects_volume),0.0)

func test_large_text_keeps_all_tasks_readable() -> void:
	get_tree().root.size=Vector2i(320,568)
	var app := app_instance()
	app.store.data.text_scale=1.15
	app.hub()
	await wait_process_frames(2)
	inspect(app)
	for entry in Catalog.modules():
		app.open_module(entry)
		var game: Control=app.learning_game
		for i in range(game.levels.size()):
			game.start_level(i)
			game.cancel_demonstration()
			await wait_process_frames(2)
			inspect(app)
	app.save()
	var saved:=Store.new();saved.load_save()
	assert_almost_eq(float(saved.data.text_scale),1.15,0.001,"Large text persists")
