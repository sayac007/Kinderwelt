extends SceneTree
const Avatar=preload("res://core/quest/custom_avatar.gd")
const Progress=preload("res://games/quest/progress.gd")
var checks:=0
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(value: bool,message: String) -> void:
	checks+=1
	if not value:failures+=1;push_error(message)
func touch(index: int,at: Vector2,pressed: bool) -> void:
	var event:=InputEventScreenTouch.new();event.index=index;event.pressed=pressed
	event.position=root.get_final_transform()*at
	Input.parse_input_event(event);await process_frame
func drag(index: int,from: Vector2,to: Vector2) -> void:
	var event:=InputEventScreenDrag.new();event.index=index
	event.position=root.get_final_transform()*to;event.relative=to-from
	Input.parse_input_event(event);await process_frame
func run() -> void:
	if OS.get_environment("KINDERWELT_CROP_TEST")!="synthetic":
		push_error("Run with tests/run.sh and isolated synthetic test data");quit(1);return
	Avatar.erase()
	var cases: Array=JSON.parse_string(FileAccess.get_file_as_string("res://tests/fixtures/avatar/orientation-cases.json"))
	for case in cases:
		var input:=FileAccess.get_file_as_bytes("res://tests/fixtures/avatar/"+case.file)
		var prepared:=Avatar.prepare(input)
		check(prepared.error=="","Actual JPEG/PNG/WebP is decoded: "+case.file)
		if prepared.error!="":continue
		check(prepared.pixels.get_size()==Vector2i(case.size[0],case.size[1]),"EXIF orientation dimensions: "+case.file)
		for probe in case.probes:
			var actual: Color=prepared.pixels.get_pixel(probe.at[0],probe.at[1])
			var expected:=Color8(probe.rgba[0],probe.rgba[1],probe.rgba[2],probe.rgba[3])
			check(absf(actual.r-expected.r)<.04 and absf(actual.g-expected.g)<.04 and absf(actual.b-expected.b)<.04,"Independent oriented color probe: "+case.file)
		check(prepared.portrait and prepared.image.get_pixel(0,0)==Color.TRANSPARENT,"Opaque source gets a cleared circular frame")
		check(maxi(prepared.image.get_width(),prepared.image.get_height())<=512 and Avatar.store(prepared.image)==OK,"Store normalized pixels only")
		var saved:=FileAccess.get_file_as_bytes(Avatar.PATH)
		for marker in ["eXIf","iTXt","tEXt","zTXt","FixtureCamera","SyntheticTestOnly","GPSLatitude"]:
			check(not saved.hex_encode().contains(marker.to_utf8_buffer().hex_encode()),"Stored image contains no source metadata: "+marker)
		var before: PackedByteArray=Avatar.texture().get_image().get_data()
		Avatar.invalidate()
		check(Avatar.texture().get_image().get_data()==before,"Restart never re-crops or shrinks saved pixels")
		check(DirAccess.get_files_at("user://avatars")==PackedStringArray(["player.png"]),"No original, URI or metadata sidecar is stored")
	for bad in [PackedByteArray([255,216,255,224]),FileAccess.get_file_as_bytes("res://tests/fixtures/avatar/orientation-1.webp").slice(0,30)]:
		check(Avatar.prepare(bad).error=="avatar_invalid","Malformed supported input fails before decoding")
	check(Avatar.prepare("not an image HEIC".to_utf8_buffer()).error=="avatar_format","Unsupported formats fail clearly")
	var legacy:=Image.create(1024,512,false,Image.FORMAT_RGBA8);legacy.fill(Color.TRANSPARENT)
	legacy.fill_rect(Rect2i(20,20,900,460),Color.WHITE)
	legacy.save_png(Avatar.PATH);Avatar.invalidate()
	check(Avatar.available() and Avatar.texture().get_image().get_data()==legacy.get_data(),"Existing 1024px cutouts survive the update without alteration")
	Avatar.erase()
	root.size=Vector2i(360,800)
	var app: Control=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
	app.store.reset();app.store.data.muted=true;app.store.data.voice_auto=false
	Progress.award(app.store.data.quest,"math_count");app.save()
	app.parents();app.manage_avatar()
	var panel: Control=app.avatar_manager
	await panel.load_path("res://tests/fixtures/avatar/orientation-1.jpg")
	for i in range(5):await process_frame
	var editor: Control=panel.preview
	check(editor.portrait and not panel.confirm_button.disabled and not Avatar.available(),"Parents preview a photo without storing it")
	check(panel.figure_button.disabled and panel.picker.filters.size()==3,"Photo has frame-only mode and native filters for three formats")
	check(panel.picker.use_native_dialog and panel.picker.access==FileDialog.ACCESS_FILESYSTEM,"Picker still uses the system dialog")
	check(Rect2(Vector2.ZERO,editor.size).encloses(Rect2(editor.circle.position,editor.circle.size)),"Crop texture stays inside its editor")
	panel.scroll.scroll_vertical=maxi(0,roundi(editor.position.y-50))
	for i in range(4):await process_frame
	var at: Vector2=editor.get_global_rect().get_center()
	await touch(0,at-Vector2(20,0),true);await touch(1,at+Vector2(20,0),true)
	await drag(1,at+Vector2(20,0),at+Vector2(60,0))
	check(editor.zoom>1.5,"Real two-finger events zoom the preview")
	await touch(0,at-Vector2(20,0),false);await touch(1,at+Vector2(60,0),false)
	var old_center: Vector2=editor.center
	await touch(0,at,true);await drag(0,at,at+Vector2(20,0));await touch(0,at+Vector2(20,0),false)
	check(editor.center.x<old_center.x,"Real drag events reposition the crop")
	var selected: Vector2=editor.center;var selected_zoom: float=editor.zoom
	root.size=Vector2i(800,360);app.update_mobile()
	for i in range(4):await process_frame
	check(editor.center==selected and editor.zoom==selected_zoom and editor.touches.is_empty(),"Rotation preserves crop and cancels stale touches")
	var expected: PackedByteArray=editor.output().get_data()
	panel.confirm_button.pressed.emit();await process_frame
	check(Avatar.available() and Avatar.texture().get_image().get_data()==expected,"Confirmed figure uses the selected crop")
	check(Progress.points(app.store.data.quest)==10 and app.store.data.hero=="custom","Import preserves points and selects custom figure")
	app.game_view.choose_hero()
	for button in app.game_view.look_buttons:check(not button.visible,"Custom image has no inappropriate wardrobe mask")
	app.game_view.open_avatar_help()
	var readonly: Control=app.game_view.avatar_panel
	check(not readonly.preview.editable and readonly.picker==null and readonly.remove_button==null,"Child chooser help has no import/editor/delete controls")
	app.go_back();await process_frame
	app.parents();app.manage_avatar();panel=app.avatar_manager
	var hash_before:=FileAccess.get_sha256(Avatar.PATH)
	await panel.load_path("res://tests/fixtures/avatar/orientation-1.webp")
	check(FileAccess.get_sha256(Avatar.PATH)==hash_before,"Replacement is not saved before adult confirmation")
	panel.close();await process_frame
	check(FileAccess.get_sha256(Avatar.PATH)==hash_before,"Cancelling keeps the existing figure")
	app.manage_avatar();panel=app.avatar_manager
	var large:=Image.create(1024,768,false,Image.FORMAT_RGBA8);large.fill(Color("4080d0"))
	panel.preview.set_source(large,true)
	for i in range(3):await process_frame
	check(Rect2(Vector2.ZERO,panel.preview.size).encloses(Rect2(panel.preview.circle.position,panel.preview.circle.size)),"Large camera images cannot expand beyond the crop viewport")
	check(app.store.reset()==OK and not FileAccess.file_exists(Avatar.PATH),"Reset removes the new photo-derived figure")
	print("AVATAR CROP: %d checks, %d failures; synthetic fixtures only; device picker NOT VERIFIED" % [checks,failures])
	if failures==0:await app.shutdown()
	else:app.audio.music.shutdown();await create_timer(.25).timeout;quit(1)
