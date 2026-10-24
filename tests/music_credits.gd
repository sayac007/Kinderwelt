extends SceneTree
var checks := 0
var failures := 0
func _initialize() -> void: call_deferred("run")
func check(value: bool, message: String) -> void:
	checks+=1
	if not value: failures+=1;push_error(message)
func run() -> void:
	var app: Control=load("res://core/quest/main.tscn").instantiate()
	root.add_child(app)
	app.store.reset();app.store.data.muted=true;app.audio.sync_settings()
	var tracks: Array=JSON.parse_string(FileAccess.get_file_as_string("res://assets/music/manifest.json")).tracks
	var licences: Array=JSON.parse_string(FileAccess.get_file_as_string("res://scripts/music/notice-license-fixtures.json"))
	var saved: Dictionary=app.store.data.duplicate(true)
	for locale in ["de","en","ru"]:
		for viewport in [Vector2i(360,800),Vector2i(800,360)]:
			root.size=viewport;app.update_mobile()
			app.store.data.locale=locale
			app.music_credits()
			for i in range(4):await process_frame
			for i in range(tracks.size()):
				var track: Dictionary=tracks[i]
				var node: Label=app.body.get_node_or_null("music_credit_"+track.id)
				check(is_instance_valid(node),"Every track has displayed credits: "+locale+"/"+track.id)
				if not is_instance_valid(node):continue
				var licence: PackedStringArray=String(licences[i]).trim_prefix("Lizenz: ").split(" · ")
				check(licence[0] in node.text and licence[1] in node.text,"Original licence/version/link visible: "+locale+"/"+track.id)
				check(track.arranger in node.text and track.source.commit in node.text and track.source.path in node.text,"Original attribution and pinned source visible: "+locale+"/"+track.id)
				check(node.size.x<=app.scroll_view.size.x+1 and node.size.y>0,"Credits wrap within the scroll view: "+locale+"/"+track.id)
				if licence[0].begins_with("CC-BY-SA-"):
					var prefix: String={"de":"Die Aufnahme in dieser App","en":"The recording in this app","ru":"Запись в этом приложении"}[locale]
					check(prefix in node.text and node.text.count(licence[1])==2,"Same-version app recording licence shown in the selected language: "+locale+"/"+track.id)
			var text: String=""
			for child in app.body.get_children():
				if child is Label:text+=child.text+"\n"
			check("GeneralUser GS 2.0.3" in text and "S. Christian Collins" in text,"Piano source attribution exists in every locale")
			check(app.store.data.quest==saved.quest and app.store.data.music_track==saved.music_track,"Reading legal credits preserves points and playlist")
			var output: String=OS.get_environment("KINDERWELT_CREDITS_OUTPUT")
			if not output.is_empty():
				if DisplayServer.get_name()=="headless":
					push_error("Actual rendering is required for credits screenshots");quit(1);return
				var first: Label=app.body.get_node("music_credit_wiener_blut")
				app.scroll_view.scroll_vertical=maxi(0,roundi(first.position.y+first.size.y-app.scroll_view.size.y+16))
				for i in range(4):await process_frame
				await RenderingServer.frame_post_draw
				var path:=output.path_join(locale+("-phone.png" if viewport.x<viewport.y else "-landscape.png"))
				check(root.get_texture().get_image().save_png(path)==OK,"Real credits screenshot saved")
	app.store.data=saved
	print("MUSIC CREDITS: %d checks, %d failures; all 20 tracks, 3 locales, 2 orientations" % [checks,failures])
	app.queue_free();await process_frame
	quit(1 if failures else 0)
