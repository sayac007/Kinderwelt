extends SceneTree
const Avatar=preload("res://core/quest/custom_avatar.gd")
const Store=preload("res://core/save_store.gd")
const Progress=preload("res://games/quest/progress.gd")
var checks := 0
var failures := 0
func check(value: bool,message: String) -> void:
	checks+=1
	if not value:failures+=1;push_error(message)
func _initialize() -> void:call_deferred("run")
func source_image() -> Image:
	var image:=Image.create(160,240,false,Image.FORMAT_RGBA8)
	image.fill(Color.TRANSPARENT)
	image.fill_rect(Rect2i(45,24,70,80),Color("ffcc66"))
	image.fill_rect(Rect2i(30,104,100,90),Color.WHITE)
	image.fill_rect(Rect2i(38,194,32,30),Color("336699"))
	image.fill_rect(Rect2i(90,194,32,30),Color("336699"))
	return image
func run() -> void:
	var mode:=OS.get_environment("KINDERWELT_AVATAR_TEST")
	if mode not in ["write","read"]:
		push_error("Run avatar tests with tests/run.sh and its isolated user directory")
		quit(1);return
	if mode=="write":
		check(Avatar.erase()==OK,"Start with no synthetic custom figure")
		var result:=Avatar.prepare(source_image().save_png_to_buffer())
		check(result.error=="","Accept a real transparent PNG")
		check(result.image.detect_alpha()!=Image.ALPHA_NONE,"Normalized figure keeps transparency")
		check(result.image.get_pixel(25,110).r>.99 and result.image.get_pixel(25,110).a>.99,"White clothing is preserved")
		var opaque:=Image.create(24,24,false,Image.FORMAT_RGBA8);opaque.fill(Color.WHITE)
		check(Avatar.prepare(opaque.save_png_to_buffer()).portrait,"Opaque RGBA PNG defaults to a round portrait")
		opaque.convert(Image.FORMAT_RGB8)
		check(Avatar.prepare(opaque.save_png_to_buffer()).portrait,"Opaque RGB PNG is accepted as a portrait")
		opaque.convert(Image.FORMAT_RGBA8);opaque.fill(Color.TRANSPARENT)
		check(Avatar.prepare(opaque.save_png_to_buffer()).error=="avatar_empty","An empty transparent image is rejected")
		check(Avatar.prepare(PackedByteArray([255,216,255,224])).error=="avatar_invalid","Truncated JPEG fails independently of its filename")
		var raw:=source_image().save_png_to_buffer()
		check(Avatar.prepare(raw.slice(0,raw.size()-9)).error=="avatar_invalid","Truncated PNG rejected before decode")
		raw[16]=0;raw[17]=0;raw[18]=32;raw[19]=0
		check(Avatar.prepare(raw).error=="avatar_too_large","Declared 8192-pixel image rejected before allocation")
		var excessive:=PackedByteArray();excessive.resize(Avatar.MAX_BYTES+1)
		check(Avatar.prepare(excessive).error=="avatar_too_large","Input byte limit enforced before decode")
		var large:=Image.create(2200,1800,false,Image.FORMAT_RGBA8);large.fill(Color.TRANSPARENT)
		large.fill_rect(Rect2i(100,100,2000,1600),Color.WHITE)
		result=Avatar.prepare(large.save_png_to_buffer())
		check(result.error=="" and maxi(result.image.get_width(),result.image.get_height())<=512,"Large valid PNG is normalized to at most 512 pixels")
		check(absf(float(result.image.get_width()-32)/(result.image.get_height()-32)-1.25)<.01,"Resize preserves proportions")
		check(Avatar.read_image("user://does-not-exist.png").error=="avatar_read_failed","Unreadable file produces a recoverable input error")
		check(Avatar.store(null)!=OK,"Invalid candidate cannot replace a stored image")
		var metadata:=FileAccess.get_file_as_bytes("res://tests/fixtures/avatar/gps-source.png")
		for marker in ["eXIf","FixtureCamera","GPSLatitude"]:
			check(metadata.hex_encode().contains(marker.to_utf8_buffer().hex_encode()),"Privacy source really contains "+marker)
		result=Avatar.prepare(metadata)
		check(result.error=="" and Avatar.store(result.image)==OK,"Process actual GPS-bearing PNG through runtime importer")
		var normalized:=FileAccess.get_file_as_bytes(Avatar.PATH)
		for marker in ["eXIf","iTXt","FixtureCamera","SyntheticTestOnly","GPSLatitude"]:
			check(not normalized.hex_encode().contains(marker.to_utf8_buffer().hex_encode()),"Stored PNG does not retain "+marker)
		var files:=DirAccess.get_files_at("user://avatars")
		check(files.size()==1 and files.has("player.png"),"Private avatar directory contains only normalized pixels, no original or metadata copy")
		Avatar.erase()
		var saved:=Store.new();saved.data.muted=true;saved.data.voice_auto=false;saved.data.quest.hero_chosen=true
		for id in ["math_count","math_count_bonus_1","math_count_bonus_2"]:Progress.award(saved.data.quest,id)
		check(Progress.points(saved.data.quest)==160 and saved.persist()==OK,"Preserve actual earned points for import tests")
		source_image().save_png("user://avatar-input.png")
	var app: Control=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
	for frame in range(6):await process_frame
	var game: Control=app.game_view
	check(Progress.points(app.store.data.quest)==160,"Points survive actual app startup")
	if mode=="write":
		game.choose_hero()
		check(game.hero_choices.size()==7,"All seven existing figures remain available before import")
		game.open_avatar_help()
		var panel: Control=game.avatar_panel
		check(panel.help_text.visible and not panel.editable,"Chooser offers read-only help")
		check(panel.picker==null and panel.choose_button==null and panel.remove_button==null,"Chooser has no file picker or image mutation controls")
		await panel.load_path("user://avatar-input.png")
		check(panel.candidate==null and not Avatar.available(),"Read-only chooser help cannot import even through its loader method")
		app.go_back();await process_frame
		check(not is_instance_valid(game.avatar_panel) and game.choosing,"Back closes import only, preserving character choice")
		app.parents();app.manage_avatar();panel=app.avatar_manager
		check(panel.editable and panel.confirm_button.disabled,"Parents area owns the editable import screen")
		await panel.load_path("user://avatar-input.png")
		check(not panel.confirm_button.disabled and panel.candidate!=null and not Avatar.available(),"Parents can preview without saving or selecting")
		panel.confirm_button.pressed.emit();await process_frame
		game=app.game_view;game.choose_hero()
		check(Avatar.available() and game.hero_choices.size()==8,"Confirm adds an eighth figure without replacing family members")
		check(app.store.data.hero=="custom" and game.custom_note.visible,"Custom figure is selected and supplied clothes are explained")
		for button in game.look_buttons:check(not button.visible,"Prepared wardrobe masks are not applied to an arbitrary image")
		game.finish_hero();await process_frame
		check(game.world.hero.person=="custom" and game.world.hero.current_texture()!=null,"Imported figure enters the playable world")
		game.open_task(0)
		check(game.task_panel.companion.person=="custom","Task companion also uses imported figure")
		game.close_task()
		app.parents();app.manage_avatar();panel=app.avatar_manager
		var old_hash:=FileAccess.get_sha256(Avatar.PATH)
		await panel.load_path("user://does-not-exist.png")
		check(panel.confirm_button.disabled and FileAccess.get_sha256(Avatar.PATH)==old_hash,"Failed replacement preserves the previous image")
		panel.remove_button.pressed.emit();await process_frame
		check(not Avatar.available() and app.store.data.hero=="wanja","Parent remove restores a family choice")
		check(FileAccess.file_exists("user://avatar-input.png") and Progress.points(app.store.data.quest)==160,"Remove never deletes source or earned points")
		app.manage_avatar();panel=app.avatar_manager
		await panel.load_path("user://avatar-input.png");panel.confirm_button.pressed.emit();await process_frame
		check(app.store.persist()==OK,"Custom selection persists for a separate-process restart")
	else:
		check(app.store.data.hero=="custom" and Avatar.available(),"New process restores custom image and selected ID")
		check(game.world.hero.person=="custom","Restart displays imported figure in the real world")
		for scene in ["landscape","home","castle","tree","seabed","city","moon"]:
			app.store.data.subject_sceneries.math=scene
			game.switch_subject("math");await process_frame
			check(game.world.hero.person=="custom" and game.world.hero.current_texture()!=null,"Custom figure plays in "+scene)
		check(Avatar.erase()==OK,"Remove test avatar after restart checks")
		var restored:=Store.new();restored.load_save()
		check(restored.data.hero=="wanja" and Progress.points(restored.data.quest)==160,"Missing avatar falls back without losing progress")
		var image: Image=Avatar.prepare(source_image().save_png_to_buffer()).image
		check(Avatar.store(image)==OK,"Restore synthetic avatar to exercise reset deletion")
		var pending:=FileAccess.open(Avatar.PATH+".tmp",FileAccess.WRITE);pending.store_buffer(image.save_png_to_buffer());pending.close()
		check(restored.reset()==OK and not FileAccess.file_exists(Avatar.PATH) and not FileAccess.file_exists(Avatar.PATH+".tmp"),"Reset removes the private avatar and any pending normalized copy")
		check(not Avatar.available() and restored.data.hero=="wanja" and Progress.points(restored.data.quest)==0,"Reset invalidates cached pixels and resets saved selection/points")
		DirAccess.remove_absolute("user://avatar-input.png")
	print("AVATAR IMPORT: ",checks," checks, ",failures," failures; ",mode,"; native Android picker still requires device testing")
	if failures==0:await app.shutdown()
	else:
		app.audio.music.shutdown();await create_timer(.25).timeout;quit(1)
