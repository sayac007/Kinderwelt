extends SceneTree
var checks:=0
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(value: bool,message: String) -> void:
	checks+=1
	if not value:failures+=1;push_error(message)
func run() -> void:
	if OS.get_environment("KINDERWELT_PRIVACY_TEST")!="synthetic":push_error("Use isolated tests/run.sh");quit(1);return
	root.size=Vector2i(360,800)
	var app: Control=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
	app.store.reset();app.store.data.muted=true;app.store.data.voice_auto=false
	preload("res://games/quest/progress.gd").award(app.store.data.quest,"math_count")
	var policy: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://assets/privacy/policy.json"))
	for locale in ["de","en","ru"]:
		app.store.data.locale=locale;app.parents()
		var before: Dictionary=app.store.data.duplicate(true)
		var open: Button=app.body.get_node("privacy_policy")
		check(open.text==app.t("privacy_policy"),"Parent policy button is localized")
		open.pressed.emit()
		for frame in range(5):await process_frame
		var text: Array=[]
		for child in app.body.get_children():
			if child is Label:text.append(child.text)
		check(text.slice(0,text.size()-1)==policy.texts[locale],"Reader displays the complete policy for the chosen language")
		check(text.back()==policy.google_privacy_url,"Google reference stays plain text")
		check(app.body.size.y>app.scroll_view.size.y,"Long policy is scrollable on a phone")
		check(app.store.data==before,"Reading does not alter progress or preferences")
		app.go_back();check(not app.privacy_reading and app.body.has_node("privacy_policy"),"Android/keyboard Back returns to parents")
	print("PRIVACY VIEW: %d checks, %d failures; offline text only" % [checks,failures])
	if failures==0:await app.shutdown()
	else:app.audio.music.shutdown();quit(1)
