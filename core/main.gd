extends Control
const Catalog = preload("res://core/catalog.gd")
const Store = preload("res://core/save_store.gd")
const Pictogram = preload("res://core/pictogram.gd")
# Test profiles can simulate a physical display without pretending to be Android.
var simulated_dpi := 0.0
var store = Store.new()
var audio = preload("res://core/cues.gd").new()
var body: VBoxContainer
var grid
var active: Dictionary = {}
var level: Dictionary = {}
var taps := 0
var play_button: Button
var status: Label
var co_play := false
var learning_game: Control
var hint_tween: Tween
const Design = preload("res://core/design.gd")
const Mobile = preload("res://core/mobile.gd")
var sound_button: Button
var scroll_view: ScrollContainer
var adventure: Control
var closing := false
var modern_view: Control
var narration = preload("res://core/modern/narration.gd").new()
var top_bar: HBoxContainer

func _ready() -> void:
	get_tree().auto_accept_quit = false
	theme = Design.make_theme()
	Mobile.configure(get_window(),simulated_dpi)
	store.load_save()
	add_child(audio)
	audio.configure(store)
	add_child(narration)
	narration.configure(store,audio.music)
	var header := HBoxContainer.new()
	top_bar = header
	header.set_anchors_and_offsets_preset(Control.PRESET_TOP_WIDE)
	header.offset_bottom = 72
	add_child(header)
	var title := Label.new()
	title.text = "  Kinderwelt"
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title.add_theme_font_size_override("font_size",27)
	header.add_child(title)
	sound_button = button("Ton an" if store.data.muted else "Ton aus", toggle_sound, header)
	sound_button.size_flags_horizontal = Control.SIZE_SHRINK_END
	sound_button.custom_minimum_size.x = 128
	var scroll := ScrollContainer.new()
	scroll_view = scroll
	scroll.follow_focus = true
	scroll.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	scroll.offset_top = 80
	add_child(scroll)
	body = VBoxContainer.new()
	body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation", 16)
	scroll.add_child(body)
	resized.connect(responsive)
	get_window().size_changed.connect(update_mobile)
	hub()
	update_mobile.call_deferred()

func update_mobile() -> void:
	Mobile.configure(get_window(),simulated_dpi)
	if OS.get_name() == "Android":
		var safe := DisplayServer.get_display_safe_area()
		var scale := Vector2(get_window().content_scale_size)/Vector2(get_window().size)
		var origin := Vector2(get_window().position)
		var top_left := (Vector2(safe.position)-origin).max(Vector2.ZERO)*scale
		var bottom := (Vector2(get_window().size)-Vector2(safe.end)+origin).max(Vector2.ZERO)*scale
		top_bar.offset_top = top_left.y
		top_bar.offset_bottom = top_left.y+72
		top_bar.offset_left = top_left.x
		top_bar.offset_right = -bottom.x
		scroll_view.offset_top = 80+top_left.y
		scroll_view.offset_bottom = -bottom.y
		scroll_view.offset_left = top_left.x
		scroll_view.offset_right = -bottom.x

func toggle_sound() -> void:
	store.data.muted = not store.data.muted
	audio.sync_settings()
	narration.sync_settings()
	sound_button.text = "Ton an" if store.data.muted else "Ton aus"
	save()

func clear() -> void:
	narration.cancel()
	if is_instance_valid(modern_view):
		if modern_view.has_method("persist"): modern_view.persist()
		remove_child(modern_view)
		modern_view.queue_free()
		modern_view = null
	if is_instance_valid(adventure):
		adventure.persist()
		remove_child(adventure)
		adventure.queue_free()
		adventure = null
	if is_instance_valid(scroll_view): scroll_view.show()
	if hint_tween: hint_tween.kill()
	learning_game = null
	grid = null
	for child in body.get_children():
		body.remove_child(child)
		child.queue_free()

func button(text: String, callback: Callable, parent: Node = body) -> Button:
	var b := Button.new()
	b.text = text
	b.tooltip_text = text
	b.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	b.custom_minimum_size = Vector2(96, 72)
	b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	b.add_theme_font_size_override("font_size", Design.font_size(26,float(store.data.text_scale)))
	b.pressed.connect(callback)
	parent.add_child(b)
	return b

func label(text: String) -> Label:
	var l := Label.new()
	l.text = text
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.add_theme_font_size_override("font_size", Design.font_size(26,float(store.data.text_scale)))
	body.add_child(l)
	return l

func sound(success := false) -> void:
	if not store.data.muted: audio.cue(success)

func save() -> void:
	if store.persist() != OK: label("Spielstand konnte nicht gespeichert werden.")

func hub() -> void:
	active = {}
	clear()
	audio.set_world("map")
	label("Dein Abenteuer")
	var tools := GridContainer.new()
	tools.columns = 2
	body.add_child(tools)
	preload("res://core/modern/icons.gd").apply(button("Figur",heroes,tools),"hero")
	preload("res://core/modern/icons.gd").apply(button("Musik",musicbox,tools),"music")
	preload("res://core/modern/icons.gd").apply(button("Klang",settings,tools),"gear")
	preload("res://core/modern/icons.gd").apply(button("Eltern",parents,tools),"parents")
	grid = preload("res://core/modern/map.gd").new()
	body.add_child(grid)
	for entry in Catalog.modules():
		var b := button("",func(): open_module(entry),grid)
		b.tooltip_text = entry.name
		var transparent := StyleBoxEmpty.new()
		b.add_theme_stylebox_override("normal",transparent)
		b.add_theme_stylebox_override("hover",transparent)
		b.add_theme_stylebox_override("pressed",transparent)
		var art := preload("res://core/modern/place_art.gd").new()
		art.place = entry.id
		art.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		art.offset_bottom = -40
		b.add_child(art)
		var caption := Label.new()
		caption.text = {"logic":"Brücken","math":"Markt","language":"Geschichten","autonomy":"Werkstatt","social":"Dorf"}[entry.id]
		caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
		caption.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
		caption.offset_top = -44
		caption.add_theme_font_size_override("font_size",Design.font_size(18,float(store.data.text_scale)))
		b.add_child(caption)
	button("💧 Die durstige Pflanze",open_water)
	button("Picos Kraftwerk · Prototyp",open_adventure)
	responsive()

func responsive() -> void:
	if is_instance_valid(grid):
		grid.columns = 1 if size.x < 600 else 2
		grid.arrange.call_deferred()

func open_module(entry: Dictionary) -> void:
	active = entry
	audio.set_world(entry.id)
	clear()
	narration.play_clip(entry.id,true)
	if entry.has("runtime"):
		learning_game = load(entry.runtime).new()
		body.add_child(learning_game)
		learning_game.setup(self, entry)
		return
	level = Catalog.level(entry)
	taps = 0
	button("⌂", hub)
	label(entry.name)
	if level.is_empty():
		label("Inhalt nicht verfügbar")
		return
	status = label("○ ○ ○")
	play_button = button("", advance)
	play_button.custom_minimum_size.y = 240
	var art := Pictogram.new()
	art.kind = entry.icon
	art.mouse_filter = Control.MOUSE_FILTER_IGNORE
	art.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	play_button.add_child(art)
	button("↻ ♪", instruct)
	button("? ☞", hint)
	button("↺", func(): open_module(entry))
	instruct()

func instruct() -> void:
	sound()
	hint()

func hint() -> void:
	if not is_instance_valid(play_button): return
	play_button.grab_focus()
	for art in play_button.get_children():
		art.lit = true
		art.queue_redraw()
	if not store.data.reduced_motion:
		if hint_tween: hint_tween.kill()
		hint_tween = create_tween()
		hint_tween.tween_property(play_button, "modulate", Color("ffdc78"), 0.25)
		hint_tween.tween_property(play_button, "modulate", Color.WHITE, 0.25)

func advance() -> void:
	if taps >= int(level.target): return
	taps += 1
	status.text = "● ".repeat(taps) + "○ ".repeat(int(level.target)-taps)
	sound(taps == int(level.target))
	if taps == int(level.target):
		status.text = "★ ★ ★"
		store.data.completed[active.id] = true
		save()
		button("⌂ ★", hub)

func settings() -> void:
	audio.sync_settings()
	sound_button.text = "Ton an" if store.data.muted else "Ton aus"
	clear()
	button("⌂", hub)
	label("Erwachsene · gemeinsam spielen ist freiwillig")
	button("Ton: " + ("aus" if store.data.muted else "an"), func():
		toggle_sound()
		settings())
	button("Große Schrift: " + ("an" if float(store.data.text_scale)>1 else "aus"), func():
		store.data.text_scale = 1.0 if float(store.data.text_scale)>1 else 1.15
		save()
		settings())
	volume_control("Musik", "music_volume")
	volume_control("Spielklänge", "effects_volume")
	volume_control("Sprache", "voice_volume")
	label("Sprachstimme: synthetischer Prototyp")
	button("Automatisch vorlesen: "+("an" if store.data.voice_auto else "aus"),func():
		store.data.voice_auto = not store.data.voice_auto
		save()
		settings())
	button("Aufgabentext: "+("an" if store.data.show_instructions else "aus"),func():
		store.data.show_instructions = not store.data.show_instructions
		save()
		settings())
	button("Weniger Bewegung: " + str(store.data.reduced_motion), func():
		store.data.reduced_motion = not store.data.reduced_motion
		save()
		settings())
	button("Gemeinsam: " + str(co_play), func():
		co_play = not co_play
		settings())
	if co_play: label("Begleiten: Was siehst du? Lass das Kind selbst tippen.")
	button("Elternbereich",parents)

func volume_control(title: String, key: String) -> void:
	label(title)
	var slider := HSlider.new()
	slider.name = key
	slider.min_value = 0.0
	slider.max_value = 1.0
	slider.step = 0.05
	slider.value = store.data[key]
	slider.custom_minimum_size = Vector2(96,72)
	slider.tooltip_text = title + " leiser oder lauter"
	body.add_child(slider)
	slider.value_changed.connect(func(value: float):
		store.data[key] = value
		audio.sync_settings()
		narration.sync_settings()
		save())

func confirm_reset() -> void:
	clear()
	label("Alle lokalen Fortschritte und Einstellungen löschen?")
	button("Abbrechen", settings)
	button("Ja, zurücksetzen", func():
		if store.reset() != OK: label("Zurücksetzen fehlgeschlagen")
		else: settings())

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		hub()
		get_viewport().set_input_as_handled()

func _notification(what: int) -> void:
	if what==NOTIFICATION_WM_CLOSE_REQUEST and is_instance_valid(body):
		shutdown()
	if what == NOTIFICATION_WM_GO_BACK_REQUEST and is_instance_valid(body):
		hub()

func open_adventure() -> void:
	clear()
	active = {}
	scroll_view.hide()
	adventure = preload("res://games/adventure/game.gd").new()
	add_child(adventure)
	adventure.setup(self)

func open_water() -> void:
	clear()
	active = {}
	scroll_view.hide()
	modern_view = preload("res://games/water/game.gd").new()
	add_child(modern_view)
	modern_view.setup(self)

func heroes() -> void:
	clear()
	button("⌂ Karte",hub)
	label("Wer begleitet dich?")
	narration.play_clip("heroes",true)
	var choices := GridContainer.new()
	choices.columns = 2
	body.add_child(choices)
	for id in preload("res://core/modern/hero.gd").PEOPLE:
		var data: Dictionary = preload("res://core/modern/hero.gd").PEOPLE[id]
		var b := button("",func():
			store.data.hero = id
			save()
			heroes()
			narration.play_clip(id),choices)
		b.custom_minimum_size = Vector2(140,230)
		b.tooltip_text = data.name
		if store.data.hero==id: b.add_theme_stylebox_override("normal",Design.style(Color("e3ead4"),Design.FOCUS))
		var hero := preload("res://core/modern/hero.tscn").instantiate()
		hero.person = id
		hero.animation = "success" if store.data.hero==id else "idle"
		hero.reduced_motion = store.data.reduced_motion
		hero.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		hero.offset_bottom = -44
		b.add_child(hero)
		if store.data.hero==id:
			var preview: WeakRef = weakref(hero)
			get_tree().create_timer(1.0).timeout.connect(func():
				var figure = preview.get_ref()
				if figure!=null: figure.animation = "idle")
		var name_label := Label.new()
		name_label.text = ("✓ " if store.data.hero==id else "")+data.name
		name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		name_label.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
		name_label.offset_top = -40
		name_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		b.add_child(name_label)
	button("Vorschau: laufen / denken",func():
		for b in choices.get_children():
			var hero: Control = b.get_child(0)
			hero.animation = "think" if hero.animation=="move" else "move")

func musicbox() -> void:
	clear()
	var box := preload("res://core/modern/musicbox.gd").new()
	body.add_child(box)
	box.setup(self)
	narration.play_clip("musicbox",true)

func parents() -> void:
	clear()
	button("⌂ Karte",hub)
	label("Für Begleitende")
	narration.play_clip("parents",true)
	label("Begleitung ist freiwillig. Lass das Kind ausprobieren. Fehler sind Hinweise.")
	button("Klang und Bedienung",settings)
	button("Lokal und offline",func():
		clear()
		button("Zurück",parents)
		label("Keine Konten, Werbung, Mikrofonaufnahmen oder Laufzeit-Netzwerkverbindungen. Spielstände bleiben auf diesem Gerät."))
	button("Spielstand zurücksetzen …",confirm_reset)

func shutdown() -> void:
	if closing: return
	closing = true
	if is_instance_valid(modern_view) and modern_view.has_method("persist"): modern_view.persist()
	if is_instance_valid(adventure): adventure.persist()
	narration.cancel()
	audio.stop()
	audio.stream = null
	audio.music.shutdown()
	# Let the audio mixer release queued streaming playbacks before engine teardown.
	await get_tree().create_timer(.25).timeout
	get_tree().quit()
