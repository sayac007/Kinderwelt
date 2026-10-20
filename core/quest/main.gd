extends Control
const Store = preload("res://core/save_store.gd")
const Mobile = preload("res://core/mobile.gd")
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
		if scroll_view.visible: label("Spielstand konnte nicht gespeichert werden.")
func toggle_sound() -> void:
	store.data.muted=not store.data.muted
	audio.sync_settings();narration.sync_settings();save()
func musicbox() -> void:
	clear()
	var box:=preload("res://core/quest/musicbox.gd").new()
	body.add_child(box);box.setup(self)
func settings() -> void:
	clear();button("Zurück zum Spiel",hub)
	label("Kinderwelt 0.5.0")
	button("Ton: "+("aus" if store.data.muted else "an"),func(): toggle_sound();settings())
	volume_control("Musik","music_volume")
	volume_control("Spielklänge","effects_volume")
	volume_control("Sprache","voice_volume")
	button("Vorlesen: "+("an" if store.data.voice_auto else "aus"),func():
		store.data.voice_auto=not store.data.voice_auto;save();settings())
	button("Weniger Bewegung: "+("an" if store.data.reduced_motion else "aus"),func():
		store.data.reduced_motion=not store.data.reduced_motion;save();settings())
	button("Große Schrift: "+("an" if store.data.text_scale>1 else "aus"),func():
		store.data.text_scale=1.0 if store.data.text_scale>1 else 1.15;save();settings())
	button("Für Erwachsene",parents)
func volume_control(title: String,key: String) -> void:
	label(title)
	var s:=HSlider.new();s.name=key
	s.min_value=0;s.max_value=1;s.step=.05;s.value=store.data[key]
	s.custom_minimum_size=Vector2(96,64);s.tooltip_text=title
	body.add_child(s)
	s.value_changed.connect(func(value):
		store.data[key]=value;audio.sync_settings();narration.sync_settings();save())
func parents() -> void:
	clear();button("Zurück zum Spiel",hub)
	label("Gemeinsam spielen ist freiwillig")
	label("Ausprobieren und noch einmal versuchen. Fehler kosten keine Sterne. Keine Zeitvorgaben, Ranglisten oder Käufe.")
	label("24 eigene Aufgaben. Keine Konten, Werbung, Mikrofonaufnahmen oder Netzwerkverbindungen. Figur und Spielstand bleiben auf diesem Gerät.")
	button("Klang & Bedienung",settings)
	button("Lokalen Spielstand löschen …",confirm_reset)
func confirm_reset() -> void:
	clear();label("Figur, Sterne und Einstellungen auf diesem Gerät löschen?")
	button("Abbrechen",parents)
	button("Ja, zurücksetzen",func():
		if store.reset()==OK: hub()
		else: label("Zurücksetzen fehlgeschlagen"))
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
