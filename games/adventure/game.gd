extends Control
const Progress = preload("res://games/adventure/progress.gd")
const World = preload("res://games/adventure/world.gd")
const Tracks = preload("res://games/adventure/tracks.gd")
var host: Control
var progress := Progress.new()
var world: Control
var overlay: PanelContainer
var room_title: Label
var feedback: Label
var track := "adventure_workshop"
var checkpoint := 0.0
var intro_page := 0
var closing := false
var toolbar: GridContainer
var navigation: HBoxContainer

func setup(parent: Control) -> void:
	host = parent
	progress.restore(host.store.data.get("adventure",{}))
	var saved_track = host.store.data.get("adventure_track",track)
	if Tracks.ITEMS.has(saved_track): track = saved_track
	host.audio.set_world(track)
	build()
	if not progress.introduced: introduction()

func _process(delta: float) -> void:
	if host == null: return
	# Use the same Android safe-area rectangle as the existing application.
	position = host.scroll_view.position
	size = host.scroll_view.size
	arrange()
	checkpoint += delta
	if checkpoint>=3:
		checkpoint = 0
		persist()

func _notification(what: int) -> void:
	if what==NOTIFICATION_APPLICATION_PAUSED and host!=null: persist()

func button(parent: Node,text: String,action: Callable) -> Button:
	var result: Button = host.button(text,action,parent)
	result.add_theme_font_size_override("font_size",preload("res://core/design.gd").font_size(19,float(host.store.data.text_scale)))
	return result
func label(parent: Node,text: String,fs := 20) -> Label:
	var result := Label.new()
	result.text = text
	result.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	result.add_theme_font_size_override("font_size",preload("res://core/design.gd").font_size(fs,float(host.store.data.text_scale)))
	parent.add_child(result)
	return result

func build() -> void:
	var layout: Control = self
	var bar := GridContainer.new()
	toolbar = bar
	bar.columns = 3
	layout.add_child(bar)
	button(bar,"⌂ Zurück",leave)
	button(bar,"? Hilfe",guide)
	button(bar,"Ⅱ Pause",pause_menu)
	room_title = label(layout, "")
	world = World.new()
	world.clip_contents = true
	world.size_flags_vertical = Control.SIZE_EXPAND_FILL
	world.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	layout.add_child(world)
	world.room = progress.room
	world.controller.position = progress.position
	world.controller.target = progress.position
	world.reduced_motion = host.store.data.reduced_motion
	world.destination.connect(interact)
	world.update_objects()
	feedback = label(layout,"Boden antippen: laufen. Maschine antippen: benutzen.",18)
	feedback.custom_minimum_size.y = 48
	feedback.max_lines_visible = 3
	feedback.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	navigation = HBoxContainer.new()
	layout.add_child(navigation)
	button(navigation,"← Raum",func(): world.move_to("left"))
	button(navigation,"⚡ Pult",func(): world.move_to("circuits" if progress.room==1 else ("sources" if progress.room==0 else "reward")))
	button(navigation,"Raum →",func(): world.move_to("right"))
	refresh()

func refresh() -> void:
	var result: Dictionary = progress.model.evaluate()
	world.powered = result.supplied and result.demand>0
	world.unlocked = progress.unlocked()
	world.source_state = progress.model.sources.duplicate()
	world.circuit_state = progress.model.circuits.duplicate()
	world.safe = result.safe
	room_title.text = "%s · %s" % [["1 · Werkstatt","2 · Kraftwerk","3 · Sternwarte"][progress.room],progress.model.difficulty]
	world.queue_redraw()

func persist() -> void:
	if not is_instance_valid(world): return
	progress.position = world.controller.position
	host.store.data.adventure = progress.capture()
	host.store.data.adventure_track = track
	if host.store.persist()!=OK: feedback.text = "Speichern fehlgeschlagen. Bitte Platz auf dem Gerät prüfen."

func leave() -> void:
	if closing: return
	closing = true
	persist()
	host.hub()

func interact(action: String) -> void:
	match action:
		"left", "right":
			var next := progress.room+(-1 if action=="left" else 1)
			if next<0:
				feedback.text = "Pico wartet in der Werkstatt. Das Kraftwerk liegt rechts."
			elif next>2: feedback.text = "Du hast die Sternwarte erreicht! Weitere Missionen folgen erst nach eurem Test."
			elif next==2 and not progress.unlocked():
				feedback.text = "Das Tor braucht Strom UND ein eingeschaltetes Relais. Schau am Schaltpult nach."
				host.sound()
			else:
				progress.room = next
				world.room = next
				world.controller.position = Vector2(150 if action=="right" else 750,365)
				world.controller.target = world.controller.position
				world.update_objects()
				feedback.text = "Sternwarte entdeckt! Tippe auf das Teleskop." if next==2 else "Erkunde die Maschinen. Die Ringe zeigen, wo du sie benutzen kannst."
				refresh()
				persist()
		"sources", "circuits": panel(action)
		"robot": introduction()
		"guide": guide()
		"reward":
			var page := dialog("Mission geschafft! ✦")
			label(page,"Pico: Du hast die Energie verteilt und die Sternwarte geöffnet. Welche andere Kombination könnte auch funktionieren?",24)
			button(page,"Sterne anschauen",close_dialog)
			button(page,"Andere Lösung ausprobieren",func(): close_dialog(); interact("left"))
			set_track("adventure_stars")

func dialog(title: String) -> VBoxContainer:
	if is_instance_valid(overlay):
		remove_child(overlay)
		overlay.queue_free()
	world.paused = true
	world.pending = ""
	overlay = PanelContainer.new()
	overlay.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(overlay)
	var style := StyleBoxFlat.new()
	style.bg_color = Color("fbf8f0")
	style.set_content_margin_all(6)
	overlay.add_theme_stylebox_override("panel",style)
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	overlay.add_child(scroll)
	var page := VBoxContainer.new()
	page.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	page.add_theme_constant_override("separation",2)
	scroll.add_child(page)
	label(page,title,22)
	return page
func close_dialog() -> void:
	if is_instance_valid(overlay):
		remove_child(overlay)
		overlay.queue_free()
	overlay = null
	world.paused = false
	refresh()
	persist()

func panel(group: String) -> void:
	var page := dialog("Energiequellen" if group=="sources" else "Leitungen & Verbraucher")
	var result: Dictionary = progress.model.evaluate()
	var limits: Dictionary = progress.model.VARIANTS[progress.model.difficulty]
	label(page,"⚡ %d erzeugt / %d benötigt\nMaterial %d/%d · Wärme %d/%d\nSicherung %d · Rest ≤ %s" % [result.power,result.demand,result.cost,limits.budget,result.heat,limits.heat,limits.fuse,str(limits.surplus) if limits.surplus<99 else "∞"],18)
	var keys := ["sun","wind","battery"] if group=="sources" else ["relay","door","lamp"]
	var names := {"sun":"☀ Sonne: +8 · Material 1 · Wärme 1","wind":"✿ Wind: +9 · Material 2 · Wärme 3","battery":"▣ Akku: +6 · Material 3 · Wärme 0","relay":"Relais: braucht 4 · Torsteuerung","door":"Tor: braucht 8 · öffnet den Weg","lamp":"Lampe: braucht 3 · nutzt Überschuss"}
	for key in keys:
		var enabled: bool = progress.model.sources[key] if group=="sources" else progress.model.circuits[key]
		var b := button(page,("✓ AN · " if enabled else "○ AUS · ")+names[key],func(): change(key); panel(group))
		b.name = key
	label(page,result.message.split(".")[0],18)
	var spacer := Control.new()
	spacer.size_flags_vertical = Control.SIZE_EXPAND_FILL
	page.add_child(spacer)
	var tabs := HBoxContainer.new()
	page.add_child(tabs)
	button(tabs,"Pult →" if group=="sources" else "Quellen",func(): panel("circuits" if group=="sources" else "sources"))
	button(tabs,"Wirkung ?",func(): diagnosis(group))
	button(tabs,"✓ Welt",close_dialog)

func change(key: String) -> void:
	if not progress.model.toggle(key): return
	var result: Dictionary = progress.model.evaluate()
	feedback.text = result.message
	if result.solved:
		var first := not progress.unlocked()
		progress.proof = progress.model.snapshot()
		if first: host.sound(true)
	else: host.sound()
	refresh()
	persist()

func diagnosis(group: String) -> void:
	var page := dialog("Pico prüft die Anlage")
	label(page,progress.model.evaluate().message,24)
	label(page,"Jede Änderung wirkt sofort. Nichts geht kaputt. Du kannst jeden Schalter wieder ausschalten.",20)
	button(page,"Zurück zu den Schaltern",func(): panel(group))
	button(page,"In die Werkstatt",close_dialog)

func guide() -> void:
	var page := dialog("Picos Bauplan")
	label(page,"Ziel: Öffne das Tor rechts im Kraftwerk.\n\n1. Quellen liefern Energie, kosten Material und erzeugen Wärme.\n2. Relais (4) UND Tor (8) einschalten. Die Lampe braucht zusätzlich 3.\n3. Beachte Material, Wärme und Sicherung. Bei Meister darf höchstens 3 Energie übrig bleiben.",20)
	button(page,"Nächster Hinweis",func(): diagnosis("sources"))
	button(page,"Selbst weiterforschen",close_dialog)

func introduction() -> void:
	var page := dialog("Hallo, ich bin Pico!")
	label(page,"Die Sternwarte ist dunkel! Hilfst du mir, das Tor mit Strom zu versorgen?\n\nTippe zum Laufen auf den Boden. Tippe auf Maschinen, um hinzugehen und sie zu benutzen.\n\nRechts geht es zum Kraftwerk. Am Quellenrad und Schaltpult kannst du experimentieren.",22)
	button(page,"Los geht’s / Überspringen",func(): progress.introduced = true; close_dialog())

func set_track(id: String) -> void:
	if not Tracks.ITEMS.has(id): return
	track = id
	host.audio.set_world(track)
	persist()
func pause_menu() -> void:
	var page := dialog("Pause · Dein Fortschritt bleibt")
	button(page,"▶ Weiterspielen",close_dialog)
	button(page,"Stufe: "+progress.model.difficulty,choose_difficulty)
	button(page,"♪ "+Tracks.ITEMS[track].title,func(): set_track("adventure_stars" if track=="adventure_workshop" else "adventure_workshop"); pause_menu())
	button(page,"Musik & Effekte regeln",audio_settings)
	button(page,"Neue Anlage …",confirm_reset)
	button(page,"⌂ Kinderwelt",leave)
func choose_difficulty() -> void:
	var page := dialog("Neue Variante? Fortschritt bleibt lokal.")
	label(page,"Die Anlage wird zurückgesetzt. Dein Weg in den anderen Spielen bleibt erhalten.",20)
	for difficulty in progress.model.VARIANTS:
		button(page,difficulty,func(): reset_mission(difficulty))
	button(page,"Abbrechen",pause_menu)
func confirm_reset() -> void:
	var page := dialog("Diese Anlage zurücksetzen?")
	label(page,"Nur diese Mission beginnt neu. Die anderen fünf Spiele bleiben erhalten.",22)
	button(page,"Ja, neue Anlage",func(): reset_mission(progress.model.difficulty))
	button(page,"Abbrechen",pause_menu)
func reset_mission(difficulty: String) -> void:
	if not progress.model.VARIANTS.has(difficulty): return
	progress = Progress.new()
	progress.model.difficulty = difficulty
	progress.introduced = true
	world.room = 0
	world.update_objects()
	world.controller.position = Vector2(180,350)
	world.controller.target = world.controller.position
	feedback.text = "Neue Anlage. Erkunde deine Möglichkeiten!"
	close_dialog()
func audio_settings() -> void:
	var page := dialog("Musik und Spielklänge")
	button(page,"Ton an" if host.store.data.muted else "Ton aus",func(): host.toggle_sound(); audio_settings())
	for key in ["music_volume","effects_volume"]:
		label(page,"Musik" if key=="music_volume" else "Effekte")
		var slider := HSlider.new()
		slider.custom_minimum_size = Vector2(96,72)
		slider.min_value = 0
		slider.max_value = 1
		slider.step = .05
		slider.value = host.store.data[key]
		slider.tooltip_text = "Musiklautstärke" if key=="music_volume" else "Effektlautstärke"
		page.add_child(slider)
		slider.value_changed.connect(func(value: float): host.store.data[key] = value; host.audio.sync_settings(); persist())
	button(page,"Zurück zur Pause",pause_menu)

func arrange() -> void:
	if not is_instance_valid(toolbar): return
	if size.y<400:
		toolbar.columns = 1
		toolbar.position = Vector2.ZERO
		toolbar.size = Vector2(112,216)
		room_title.position = Vector2(0,220)
		room_title.size = Vector2(112,60)
		room_title.text = ["Werkstatt","Kraftwerk","Sternwarte"][progress.room]+"\n"+progress.model.difficulty
		feedback.position = Vector2(120,0)
		feedback.size = Vector2(size.x-120,60)
		world.position = Vector2(120,64)
		world.size = Vector2(size.x-120,maxf(40,size.y-140))
		navigation.position = Vector2(120,size.y-72)
		navigation.size = Vector2(size.x-120,72)
	else:
		toolbar.columns = 3
		toolbar.position = Vector2.ZERO
		toolbar.size = Vector2(size.x,72)
		room_title.position = Vector2(0,76)
		room_title.size = Vector2(size.x,28)
		room_title.text = "%s · %s" % [["1 · Werkstatt","2 · Kraftwerk","3 · Sternwarte"][progress.room],progress.model.difficulty]
		world.position = Vector2(0,108)
		world.size = Vector2(size.x,maxf(40,size.y-260))
		feedback.position = Vector2(0,size.y-148)
		feedback.size = Vector2(size.x,72)
		navigation.position = Vector2(0,size.y-72)
		navigation.size = Vector2(size.x,72)
