extends Control
const Store = preload("res://core/save_store.gd")
const Mobile = preload("res://core/mobile.gd")
const Lang = preload("res://core/quest/language.gd")
var simulated_dpi := 0.0
var store = Store.new()
var audio = preload("res://core/cues.gd").new()
var narration = preload("res://core/quest/narration.gd").new()
var body: VBoxContainer
var scroll_view: ScrollContainer
var game_view: Control
var closing := false
func _ready() -> void:
	get_tree().auto_accept_quit=false
	theme=preload("res://core/quest/theme.gd").make_theme()
	Mobile.configure(get_window(),simulated_dpi)
	store.load_save()
	add_child(audio);audio.configure(store)
	add_child(narration);narration.configure(store,audio.music)
	scroll_view=ScrollContainer.new()
	scroll_view.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	scroll_view.follow_focus=true
	add_child(scroll_view)
	body=VBoxContainer.new()
	body.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation",14)
	scroll_view.add_child(body)
	get_window().size_changed.connect(update_mobile)
	hub()
	update_mobile.call_deferred()
func update_mobile() -> void:
	Mobile.configure(get_window(),simulated_dpi)
	if not is_instance_valid(scroll_view): return
	scroll_view.offset_left=12;scroll_view.offset_right=-12
	scroll_view.offset_top=8;scroll_view.offset_bottom=-8
	if OS.get_name()=="Android":
		var safe:=DisplayServer.get_display_safe_area()
		var ratio:=Vector2(get_window().content_scale_size)/Vector2(get_window().size)
		var origin:=Vector2(get_window().position)
		var a: Vector2=(Vector2(safe.position)-origin).max(Vector2.ZERO)*ratio
		var b: Vector2=(Vector2(get_window().size)-Vector2(safe.end)+origin).max(Vector2.ZERO)*ratio
		scroll_view.offset_left+=a.x;scroll_view.offset_top+=a.y
		scroll_view.offset_right-=b.x;scroll_view.offset_bottom-=b.y
	if is_instance_valid(game_view): game_view.arrange.call_deferred()
func clear() -> void:
	narration.cancel()
	if is_instance_valid(game_view):
		game_view.persist()
		remove_child(game_view);game_view.queue_free();game_view=null
	scroll_view.show()
	scroll_view.scroll_vertical=0
	for child in body.get_children(): body.remove_child(child);child.queue_free()
func hub() -> void:
	clear()
	scroll_view.hide()
	game_view=preload("res://games/quest/game.gd").new()
	add_child(game_view);game_view.setup(self)
func button(caption: String,action: Callable,parent: Node=body) -> Button:
	var b:=Button.new()
	b.text=caption;b.tooltip_text=caption
	b.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	b.custom_minimum_size=Vector2(96,64)
	b.size_flags_horizontal=Control.SIZE_EXPAND_FILL
	b.add_theme_font_size_override("font_size",roundi(22*store.data.text_scale))
	b.pressed.connect(action);parent.add_child(b)
	return b
func label(caption: String) -> Label:
	var l:=Label.new();l.text=caption
	l.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	l.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	l.add_theme_font_size_override("font_size",roundi(21*store.data.text_scale))
	body.add_child(l);return l
func sound(success:=false) -> void: audio.cue(success)
func save() -> void:
	if store.persist()!=OK:
		push_warning("Local progress could not be saved")
		if scroll_view.visible: label(t("save_error"))
func toggle_sound() -> void:
	store.data.muted=not store.data.muted
	audio.sync_settings();narration.sync_settings();save()
func musicbox() -> void:
	clear()
	var box:=preload("res://core/quest/musicbox.gd").new()
	body.add_child(box);box.setup(self)
func t(key: String) -> String: return Lang.text(key,store.data.locale)
func flag(key: String,value: bool) -> String: return t(key)+": "+t("on" if value else "off")
func subjects() -> void:
	clear();button(t("back"),hub)
	for subject in preload("res://games/quest/progress.gd").SUBJECTS:
		button(t(subject),func(): hub();game_view.switch_subject(subject))
func languages() -> void:
	clear();button(t("back"),hub)
	label(t("select_language"))
	for locale in Lang.LOCALES:
		button(("✓ " if locale==store.data.locale else "")+Lang.NAMES[locale],func():
			store.data.locale=locale;save();hub())
func settings() -> void:
	clear();button(t("back"),hub)
	label("Kinderwelt 0.6.0")
	button(t("language"),languages)
	button(flag("sound",not store.data.muted),func(): toggle_sound();settings())
	volume_control(t("music"),"music_volume")
	volume_control(t("effects"),"effects_volume")
	volume_control(t("voice"),"voice_volume")
	button(flag("autovoice",store.data.voice_auto),func():
		store.data.voice_auto=not store.data.voice_auto;save();settings())
	button(flag("less_motion",store.data.reduced_motion),func():
		store.data.reduced_motion=not store.data.reduced_motion;save();settings())
	button(flag("large_text",store.data.text_scale>1),func():
		store.data.text_scale=1.0 if store.data.text_scale>1 else 1.15;save();settings())
	button(t("adults"),parents)
func volume_control(title: String,key: String) -> void:
	label(title)
	var s:=HSlider.new();s.name=key
	s.min_value=0;s.max_value=1;s.step=.05;s.value=store.data[key]
	s.custom_minimum_size=Vector2(96,64);s.tooltip_text=title
	body.add_child(s)
	s.value_changed.connect(func(value):
		store.data[key]=value;audio.sync_settings();narration.sync_settings();save())
func parents() -> void:
	clear();button(t("back"),hub)
	label(t("voluntary"))
	label(t("respect"))
	label(t("privacy"))
	button(t("controls"),settings)
	button(t("music_sources"),music_credits)
	button(t("reset"),confirm_reset)
func music_credits() -> void:
	clear();button(t("return"),parents)
	label(t("music_sources"))
	label(t("classical_note"))
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/music/manifest.json"))
	for track in manifest.tracks:
		label(track.composer+" · "+track.title)
		label(track.arranger+"\n"+track.license)
		label(track.source.repository+"\n"+track.source.path)
	label(t("piano_credit"))
func confirm_reset() -> void:
	clear();label(t("reset_question"))
	button(t("cancel"),parents)
	button(t("reset_yes"),func():
		if store.reset()==OK: hub()
		else: label(t("reset_error")))
func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"): hub();get_viewport().set_input_as_handled()
func _notification(what: int) -> void:
	if not is_instance_valid(body): return
	if what==NOTIFICATION_WM_GO_BACK_REQUEST: hub()
	elif what==NOTIFICATION_WM_CLOSE_REQUEST: shutdown()
func shutdown() -> void:
	if closing: return
	closing=true
	if is_instance_valid(game_view): game_view.persist()
	narration.cancel();audio.stop();audio.stream=null;audio.music.shutdown()
	await get_tree().create_timer(.25).timeout
	get_tree().quit()
