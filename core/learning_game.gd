extends VBoxContainer
const Art = preload("res://core/world_art.gd")
const Design = preload("res://core/design.gd")
const Catalog = preload("res://core/catalog.gd")
const Progress = preload("res://core/learning_progress.gd")
var host: Control
var entry: Dictionary
var levels: Array = []
var index := -1
var model: RefCounted
var selected := -1
var hint_stage := 0
var assisted := false
var recorded := false
var gesture: Array = []
var rejected := -1
var source_buttons: Array[Button] = []
var socket_buttons: Array[Button] = []
var instruction_art: Control
var undo_button: Button
var next_button: Button
var feedback := ""
var session := 0
var demonstrating := false
var layout_grids: Array[GridContainer] = []
var entering_level := false

func setup(app: Control, registration: Dictionary) -> void:
	host = app
	entry = registration
	levels = Catalog.levels(entry)
	add_theme_constant_override("separation", 12)
	host.resized.connect(responsive)
	chooser()

func wipe() -> void:
	source_buttons.clear()
	socket_buttons.clear()
	layout_grids.clear()
	for child in get_children():
		remove_child(child)
		child.queue_free()

func text(value: String, parent: Node = self) -> Label:
	var l := Label.new()
	l.text = value
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.add_theme_font_size_override("font_size", Design.font_size(23,float(host.store.data.text_scale)))
	parent.add_child(l)
	return l

func art_button(spec: Dictionary, tooltip: String, action: Callable, parent: Node = self, minimum := Vector2(96,112)) -> Button:
	var b := Button.new()
	var compact: bool = spec.get("kind", "") in ["home","levels","retry","undo","replay","hint","next","test","previous","forward"]
	var large_text: bool = float(host.store.data.text_scale)>1
	b.custom_minimum_size = Vector2(96,112 if large_text else 80) if compact else minimum
	b.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	b.tooltip_text = tooltip
	b.pressed.connect(action)
	parent.add_child(b)
	var art := create_art()
	art.spec = spec.merged({"reduced_motion": host.store.data.reduced_motion})
	art.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	b.add_child(art)
	var caption := Label.new()
	caption.text = short_caption(spec,tooltip)
	caption.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	caption.mouse_filter = Control.MOUSE_FILTER_IGNORE
	caption.add_theme_font_size_override("font_size",Design.font_size(18,float(host.store.data.text_scale)))
	caption.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
	caption.offset_top = (-56 if large_text else -32) if compact else (-64 if large_text else -56)
	caption.offset_left = 4
	caption.offset_right = -4
	b.add_child(caption)
	art.offset_bottom = caption.offset_top
	return b

func picture(spec: Dictionary, height := 160.0) -> Control:
	var art := create_art()
	art.spec = spec.merged({"reduced_motion": host.store.data.reduced_motion})
	art.custom_minimum_size.y = minf(height,host.size.x*0.6) if host.size.x<600 else height
	add_child(art)
	return art

func short_caption(spec: Dictionary, tooltip: String) -> String:
	var captions := {"home":"Start", "levels":"Aufgaben", "retry":"Nochmal", "undo":"Zurück", "replay":"Anleitung", "hint":"Hilfe", "next":"Weiter", "test":"Los!", "previous":"Zurück", "forward":"Weiter"}
	var kind: String = spec.get("kind","")
	if captions.has(kind): return captions[kind]
	if kind == "piece": return "1 Feld" if int(spec.amount)==1 else "%d Felder" % int(spec.amount)
	if kind == "fruit": return tooltip
	if kind == "bridge": return "Hier bauen"
	if kind == "basket": return "%d von %d" % [int(spec.get("amount",0)),int(spec.target)]
	if kind == "level": return "Aufgabe %d" % int(spec.ordinal)
	if kind == "setting":
		var titles := {"ramp":["Neigung","Boden"],"light":["Richtung","Blende"],"water":["Wasserweg","Ventil"],"wind":["Segel","Wind"],"balance":["Links","Rechts"],"garden":["Wasser","Sonne"]}
		var value_names := {"ramp":[[],["Glatt","Rau"]],"light":[["Nach oben","Zur Mitte","Zur Pflanze"],["Blende zu","Blende auf"]],"water":[["Nach links","Zur Blume","Nach rechts"],["Ventil zu","Ventil auf"]],"wind":[["Kein Segel","Kleines Segel","Großes Segel"],["Windstill","Leichter Wind","Viel Wind"]],"garden":[["Kein Wasser","Etwas Wasser","Viel Wasser"],["Wolken","Etwas Sonne","Viel Sonne"]]}
		if value_names.has(spec.experiment):
			var choices: Array = value_names[spec.experiment][int(spec.control)]
			if not choices.is_empty(): return choices[int(spec.value)]
		return titles[spec.experiment][int(spec.control)]+" · "+str(int(spec.value))
	if kind == "story":
		var words := {"garden":["Der Samen","Wasser","Der Trieb","Die Blume"],"bread":["Das Mehl","Der Teig","Im Ofen","Das Brot"],"rain":["Regen","Der Schirm","Sonne"],"kite":["Papier","Falten","Die Schnur","Fliegen"],"paint":["Papier","Malen","Sonne"],"picnic":["Der Korb","Der Apfel","Zuklappen","Tragen","Teilen"]}
		return words[spec.card.scene][int(spec.card.step)]
	if kind == "adult": return "Gemeinsam"
	if kind == "story_slot": return "Platz %d" % int(spec.ordinal)
	return tooltip

func create_art() -> Control:
	return Art.new()

func row() -> HBoxContainer:
	var result := HBoxContainer.new()
	result.add_theme_constant_override("separation",8)
	add_child(result)
	return result

func make_grid() -> GridContainer:
	var result := GridContainer.new()
	result.add_theme_constant_override("h_separation",8)
	result.add_theme_constant_override("v_separation",8)
	add_child(result)
	layout_grids.append(result)
	return result

func responsive() -> void:
	for group in layout_grids:
		if is_instance_valid(group): group.columns = 3 if host.size.x < 600 else 5

func chooser() -> void:
	cancel_demonstration()
	index = -1
	wipe()
	art_button({"kind":"home"}, "Zurück zur Kinderwelt", host.hub)
	text(entry.name)
	if levels.is_empty():
		text("Inhalt nicht verfügbar")
		return
	var progress := Progress.state(host.store, entry.id)
	text("Dein Vorschlag · " + "● ".repeat(int(progress.tier)))
	art_button({"kind":"next"}, "Mit dem vorgeschlagenen Level spielen", func(): start_level(Progress.recommend(host.store, entry.id, levels)))
	for tier in range(1,4):
		text("● ".repeat(tier))
		var group := make_grid()
		var ordinal := 0
		for i in range(levels.size()):
			if levels[i].tier != tier: continue
			ordinal += 1
			art_button({"kind":"level","tier":tier,"ordinal":ordinal,"done":progress.completed.has(levels[i].id)}, "Stufe %d · Aufgabe %d" % [tier,ordinal], start_level.bind(i), group)
	responsive()

func start_level(which: int) -> void:
	if which < 0 or which >= levels.size(): return
	cancel_demonstration()
	index = which
	model = create_model(levels[index])
	selected = -1
	hint_stage = 0
	assisted = false
	recorded = false
	gesture = []
	rejected = -1
	feedback = ""
	# A new task must not inherit the chooser's scroll position or focus the
	# bottom inventory before its instruction has been seen.
	var scroll := get_parent().get_parent() as ScrollContainer
	if scroll: scroll.scroll_vertical = 0
	entering_level = true
	build()
	replay()
	entering_level = false

func create_model(_data: Dictionary) -> RefCounted:
	return null

func build() -> void:
	wipe()
	var navigation := row()
	art_button({"kind":"home"}, "Zurück zur Kinderwelt", host.hub, navigation)
	art_button({"kind":"levels"}, "Alle Aufgaben", chooser, navigation)
	art_button({"kind":"retry"}, "Noch einmal", func(): start_level(index), navigation)
	text(entry.name + " · Aufgabe %d" % [index+1])
	text(instruction_text())
	instruction_art = null
	build_board()
	if not socket_buttons.is_empty(): instruction_art = socket_buttons[0].get_child(0)
	var controls := row()
	undo_button = art_button({"kind":"undo","hint":gesture==[-1,-1]}, "Letzten Schritt rückgängig machen", undo, controls)
	art_button({"kind":"replay"}, "Anleitung wiederholen", replay, controls)
	art_button({"kind":"hint","stage":mini(hint_stage,2)}, "Hilfe: zeigen, ein Schritt, vormachen", hint, controls)
	if not feedback.is_empty(): text(feedback)
	if model.complete():
		picture({"kind":"success"},80)
		next_button = art_button({"kind":"next"}, "Nächste vorgeschlagene Aufgabe", func(): start_level(Progress.recommend(host.store, entry.id, levels)))
	responsive()
	if model.complete():
		next_button.grab_focus()
	elif entering_level:
		navigation.get_child(0).grab_focus()
	elif not source_buttons.is_empty():
		for b in source_buttons:
			if not b.disabled:
				b.grab_focus()
				break
	elif not socket_buttons.is_empty(): socket_buttons[0].grab_focus()

func instruction_text() -> String:
	if entry.id == "logic": return "Bau die Brücke. Wähle Holz und tippe auf die Lücke!"
	match levels[index].get("mode",""):
		"compare": return "In welchem Korb liegt am meisten Obst?"
		"share": return "Verteile das Obst auf beide Körbe!"
		"sort": return "Lege jede Frucht in ihren Korb!"
	return "Fülle die Körbe. Die Umrisse zeigen, wie viel fehlt."

func build_board() -> void:
	pass

func replay() -> void:
	host.sound()
	if is_instance_valid(instruction_art):
		instruction_art.spec.hint = true
		instruction_art.queue_redraw()
		if not host.store.data.reduced_motion:
			var animation := instruction_art.create_tween()
			animation.tween_property(instruction_art,"phase",1.0,0.3)
			animation.tween_property(instruction_art,"phase",0.0,0.3)

func pick(piece: int) -> void:
	cancel_demonstration()
	if model.complete(): return
	selected = piece if selected != piece else -1
	gesture = []
	rejected = -1
	feedback = ""
	build()
	if selected >= 0 and not socket_buttons.is_empty(): socket_buttons[0].grab_focus()

func socket(slot: int) -> void:
	cancel_demonstration()
	if model.complete(): return
	var accepted := false
	if levels[index].get("mode") == "compare": accepted = model.choose(slot)
	elif selected >= 0: accepted = model.place(selected,slot)
	if accepted:
		selected = -1
		rejected = -1
		gesture = []
		feedback = ""
		host.sound(model.complete())
		finish_if_complete()
	else:
		rejected = slot
		host.sound()
		# Keep the selected piece visible beside the unchanged target for comparison.
		feedback = "Schau auf die Umrisse. Du kannst es weiter versuchen."
	build()

func undo() -> void:
	cancel_demonstration()
	model.undo()
	selected = -1
	gesture = []
	rejected = -1
	feedback = ""
	build()

func hint() -> void:
	if demonstrating: return
	if model.complete():
		replay()
		return
	assisted = true
	hint_stage = mini(hint_stage+1,3)
	gesture = model.next_hint()
	if hint_stage == 2: help_one()
	elif hint_stage == 3:
		demonstrating = true
		var token := session
		for _step in range(64):
			if model.complete(): break
			gesture = model.next_hint()
			build()
			if not host.store.data.reduced_motion:
				await get_tree().create_timer(0.45).timeout
				if not is_inside_tree() or session != token: return
			help_one()
			host.sound()
		demonstrating = false
	finish_if_complete()
	build()
	if hint_stage == 1:
		if gesture.size() == 2:
			if gesture[0] >= 0 and gesture[0] < source_buttons.size(): source_buttons[gesture[0]].grab_focus()
			elif gesture[0] >= 0 and gesture[0] < socket_buttons.size(): socket_buttons[gesture[0]].grab_focus()
			else: undo_button.grab_focus()
	host.sound(model.complete())

func help_one() -> void:
	var move: Array = model.next_hint()
	if move.is_empty(): return
	if move == [-1,-1]: model.undo()
	elif levels[index].get("mode") == "compare": model.choose(move[0])
	else: model.place(move[0],move[1])
	selected = -1
	gesture = []
	rejected = -1

func finish_if_complete() -> void:
	if model.complete() and not recorded:
		recorded = true
		Progress.record(host.store, entry.id, levels[index], assisted)
		host.save()

func cancel_demonstration() -> void:
	session += 1
	demonstrating = false

func _exit_tree() -> void:
	cancel_demonstration()
