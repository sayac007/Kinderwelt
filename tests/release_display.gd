extends SceneTree
var checks:=0
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(value: bool,message: String) -> void:
	checks+=1
	if not value:failures+=1;push_error(message)
func run() -> void:
	if OS.get_environment("KINDERWELT_RELEASE_UI_TEST")!="synthetic":push_error("Use isolated tests/run.sh");quit(1);return
	var app: Control=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
	app.store.reset();app.store.data.muted=true;app.store.data.voice_auto=false
	preload("res://games/quest/progress.gd").award(app.store.data.quest,"math_count")
	for locale in ["de","en","ru"]:
		app.store.data.locale=locale
		var before: Dictionary=app.store.data.duplicate(true)
		app.parents()
		var shown: Label=app.body.get_node("release_version")
		check(shown.text.contains(str(ProjectSettings.get_setting("application/config/version"))),"Parent display uses canonical version")
		check(shown.text.ends_with(str(ProjectSettings.get_setting("application/config/version_code"))),"Parent display uses canonical version code")
		check(shown.text.begins_with(app.t("app_version")),"Version label is localized")
		check(shown.get_theme_font_size("font_size")==16,"Version stays unobtrusive")
		check(app.store.data==before,"Opening parents preserves all points and preferences")
	print("RELEASE DISPLAY: %d checks, %d failures; no telemetry or release credentials" % [checks,failures])
	if failures==0:await app.shutdown()
	else:app.audio.music.shutdown();quit(1)
