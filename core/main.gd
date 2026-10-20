extends Control
const Catalog = preload("res://core/catalog.gd")
const Store = preload("res://core/save_store.gd")
const Pictogram = preload("res://core/pictogram.gd")
var store = Store.new()
var audio = preload("res://core/cues.gd").new()
var body: VBoxContainer
var grid: GridContainer
var active: Dictionary = {}
var level: Dictionary = {}
var taps := 0
var play_button: Button
var status: Label
var co_play := false
var learning_game: Control
var hint_tween: Tween

func _ready() -> void:
	store.load_save()
	add_child(audio)
	var scroll := ScrollContainer.new()
	scroll.follow_focus = true
	scroll.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(scroll)
	body = VBoxContainer.new()
	body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation", 16)
	scroll.add_child(body)
	resized.connect(responsive)
	hub()

func clear() -> void:
	if hint_tween: hint_tween.kill()
	learning_game = null
	grid = null
	for child in body.get_children():
		body.remove_child(child)
		child.queue_free()

func button(text: String, callback: Callable, parent: Node = body) -> Button:
	var b := Button.new()
	b.text = text
	b.custom_minimum_size = Vector2(96, 72)
	b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	b.add_theme_font_size_override("font_size", 26)
	b.pressed.connect(callback)
	parent.add_child(b)
	return b

func label(text: String) -> Label:
	var l := Label.new()
	l.text = text
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.add_theme_font_size_override("font_size", 26)
	body.add_child(l)
	return l

func sound(success := false) -> void:
	if not store.data.muted: audio.cue(success)

func save() -> void:
	if store.persist() != OK: label("Spielstand konnte nicht gespeichert werden.")

func hub() -> void:
	active = {}
	clear()
	label("Kinderwelt")
	grid = GridContainer.new()
	body.add_child(grid)
	for entry in Catalog.modules():
		var b := button("", func(): open_module(entry), grid)
		b.tooltip_text = entry.name
		var caption := Label.new()
		caption.text = preload("res://core/localization.gd").message(entry.name_key) if entry.has("name_key") else entry.name
		caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
		caption.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
		caption.offset_top = -40
		b.add_child(caption)
		b.custom_minimum_size.y = 160
		var art := Pictogram.new()
		art.kind = entry.icon
		art.mouse_filter = Control.MOUSE_FILTER_IGNORE
		art.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		# Leave the lower area clear for the optional text label.
		art.offset_bottom = -45
		b.add_child(art)
		b.alignment = HORIZONTAL_ALIGNMENT_CENTER
		b.vertical_icon_alignment = VERTICAL_ALIGNMENT_TOP
	button("⚙ Erwachsene", settings)
	responsive()
	grid.get_child(0).grab_focus()

func responsive() -> void:
	if is_instance_valid(grid): grid.columns = 1 if size.x < 600 else 2

func open_module(entry: Dictionary) -> void:
	active = entry
	clear()
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
	clear()
	button("⌂", hub)
	label("Erwachsene · gemeinsam spielen ist freiwillig")
	button("Ton: " + ("aus" if store.data.muted else "an"), func():
		store.data.muted = not store.data.muted
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
	button("Spielstand zurücksetzen …", confirm_reset)

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
	if what == NOTIFICATION_WM_GO_BACK_REQUEST and is_instance_valid(body):
		hub()
