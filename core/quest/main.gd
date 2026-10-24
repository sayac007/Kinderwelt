extends Control
const Store = preload("res://core/save_store.gd")
const Mobile = preload("res://core/mobile.gd")
const Lang = preload("res://core/quest/language.gd")
var simulated_dpi := 0.0
var store = Store.new()
var audio = preload("res://core/cues.gd").new()
var narration = preload("res://core/quest/narration.gd").new()
var scenery_grid: GridContainer
var body: VBoxContainer
var scroll_view: ScrollContainer
var game_view: Control
var avatar_manager: Control
var closing := false
var layout_pending := false
var updating_layout := false
var praise_cursor := randi()%6
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
	get_window().size_changed.connect(request_layout)
	hub()
	update_mobile.call_deferred()
func request_layout() -> void:
	if layout_pending or closing: return
	layout_pending=true
	settle_layout.call_deferred()
func settle_layout() -> void:
	await get_tree().process_frame
	if not is_inside_tree() or closing: return
	update_mobile()
	await get_tree().process_frame
	if not is_inside_tree() or closing: return
	update_mobile()
	layout_pending=false
func update_mobile() -> void:
	if updating_layout: return
	updating_layout=true
	Mobile.configure(get_window(),simulated_dpi)
	if not is_instance_valid(scroll_view):
		updating_layout=false
		return
	scroll_view.offset_left=12;scroll_view.offset_right=-12
	scroll_view.offset_top=8;scroll_view.offset_bottom=-8
	if OS.get_name()=="Android":
		var inset:=Mobile.safe_insets(get_window().size,get_window().content_scale_size,DisplayServer.get_display_safe_area(),get_window().position)
		scroll_view.offset_left+=inset.x;scroll_view.offset_top+=inset.y
		scroll_view.offset_right-=inset.z;scroll_view.offset_bottom-=inset.w
	if is_instance_valid(game_view): game_view.arrange.call_deferred()
	if is_instance_valid(scenery_grid): scenery_grid.columns=2 if scroll_view.size.x<640 else 4
	updating_layout=false
func praise_id() -> String:
	var result := "praise_"+str(praise_cursor)
	praise_cursor=(praise_cursor+1)%6
	return result

func clear() -> void:
	narration.cancel()
	if is_instance_valid(avatar_manager):
		remove_child(avatar_manager);avatar_manager.queue_free();avatar_manager=null
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
func sceneries() -> void:
	var subject: String=store.data.quest.subject
	clear();button(t("back"),hub)
	label(t("scenery")+" · "+t(subject))
	label(t("scenery_per_subject"))
	scenery_grid=GridContainer.new();scenery_grid.columns=2 if scroll_view.size.x<640 else 4
	scenery_grid.add_theme_constant_override("h_separation",10)
	scenery_grid.add_theme_constant_override("v_separation",10)
	body.add_child(scenery_grid)
	for id in preload("res://core/quest/scenery.gd").CHOICES:
		var card:=preload("res://core/quest/scenery_card.gd").new()
		card.scenery=id;card.chosen=store.data.subject_sceneries[subject]==id
		card.custom_minimum_size=Vector2(130,138)
		card.size_flags_horizontal=Control.SIZE_EXPAND_FILL
		card.tooltip_text=t("scene_"+id)
		card.accessibility_name=t("scene_"+id)
		card.accessibility_description=t(subject)
		card.pressed.connect(func():store.data.subject_sceneries[subject]=id;save();hub())
		scenery_grid.add_child(card)
		var caption:=Label.new();caption.text=t("scene_"+id)
		caption.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
		caption.add_theme_font_size_override("font_size",16)
		caption.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
		caption.mouse_filter=Control.MOUSE_FILTER_IGNORE
		caption.set_anchors_and_offsets_preset(PRESET_BOTTOM_WIDE)
		caption.offset_top=-52;caption.offset_bottom=-5
		card.add_child(caption)
func languages() -> void:
	clear();button(t("back"),hub)
	label(t("select_language"))
	for locale in Lang.LOCALES:
		button(("✓ " if locale==store.data.locale else "")+Lang.locale_name(locale,store.data.locale),func():
			store.data.locale=locale;save();hub())
func settings() -> void:
	clear();button(t("back"),hub)
	label(("Мир детства" if store.data.locale=="ru" else "Kinderwelt")+" "+str(ProjectSettings.get_setting("application/config/version","")))
	button(t("language"),languages)
	button(t("scenery"),sceneries)
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
	var version:=label(t("app_version")+" "+str(ProjectSettings.get_setting("application/config/version"))+" · "+t("app_version_code")+" "+str(ProjectSettings.get_setting("application/config/version_code")))
	version.name="release_version"
	version.add_theme_font_size_override("font_size",roundi(16*store.data.text_scale))
	label(t("voluntary"))
	label(t("respect"))
	label(t("privacy"))
	button(t("avatar_manage"),manage_avatar)
	if store.data.quest.archived.size()<preload("res://games/quest/progress.gd").legacy_rewards().size():
		button(t("restore_old_round"),confirm_old_round)
	button(t("controls"),settings)
	button(t("music_sources"),music_credits)
	button(t("reset"),confirm_reset)
func manage_avatar() -> void:
	clear();scroll_view.hide()
	avatar_manager=preload("res://core/quest/avatar_import.gd").new()
	add_child(avatar_manager);avatar_manager.setup(self,true,true)
	avatar_manager.closed.connect(parents)
	avatar_manager.imported.connect(func():
		store.data.hero="custom";store.data.quest.hero_chosen=true;save();hub())
	avatar_manager.removed.connect(func():
		if store.data.hero=="custom":store.data.hero="wanja"
		save();parents())
func confirm_old_round() -> void:
	clear();label(t("restore_old_explanation"))
	button(t("cancel"),parents)
	button(t("restore_old_confirm"),func():
		for id in preload("res://games/quest/progress.gd").legacy_rewards():store.data.quest.archived[id]=true
		store.data.quest.total_points=preload("res://games/quest/progress.gd").points(store.data.quest)
		save();hub())
func music_credits() -> void:
	clear();button(t("return"),parents)
	label(t("music_sources"))
	label(t("classical_note"))
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/music/manifest.json"))
	for track in manifest.tracks:
		if store.data.locale=="ru":
			var names: Dictionary=Lang.data().music.get(track.id,{})
			label(names.get("composer","")+" · "+names.get("title",""))
		else:
			label(track.composer+" · "+track.title)
		# Preserve original author names and legal identifiers in every locale.
		# URLs are displayed as text; this screen performs no network access.
		var source_url: String=track.source.repository.trim_suffix(".git")+"/blob/"+track.source.commit+"/"+track.source.path
		var text: String=track.arranger+"\n"+track.license+" · "+track.license_url+"\n"+source_url
		if track.has("recording_license"):
			text+="\n"+track.recording_license.notices[store.data.locale]
		var credit:=label(text)
		credit.name="music_credit_"+track.id
	if store.data.locale=="ru":label("GeneralUser GS 2.0.3 · S. Christian Collins")
	label(t("piano_credit"))
func confirm_reset() -> void:
	clear();label(t("reset_question"))
	label(t("avatar_reset_note"))
	button(t("cancel"),parents)
	button(t("reset_yes"),func():
		if store.reset()==OK: hub()
		else: label(t("reset_error")))
func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"): go_back();get_viewport().set_input_as_handled()
func go_back() -> void:
	if is_instance_valid(avatar_manager):avatar_manager.handle_back();return
	if is_instance_valid(game_view) and game_view.handle_avatar_back():return
	hub()
func _notification(what: int) -> void:
	if not is_instance_valid(body): return
	if what==NOTIFICATION_WM_GO_BACK_REQUEST: go_back()
	elif what==NOTIFICATION_WM_CLOSE_REQUEST: shutdown()
func shutdown() -> void:
	if closing: return
	closing=true
	if is_instance_valid(game_view): game_view.persist()
	narration.cancel();audio.stop();audio.stream=null;audio.music.shutdown()
	await get_tree().create_timer(.25).timeout
	get_tree().quit()
