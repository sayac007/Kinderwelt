extends Control
const Model = preload("res://games/water/model.gd")
const Board = preload("res://games/water/board.gd")
var host: Control
var model := Model.new()
var board: Control
var toolbar: GridContainer
var controls: GridContainer
var message: Label
var mode_button: Button
var water_button: Button
var move_mode := false
var selected := -1
var completed := false
var proof := {}
var choice_panel: PanelContainer
const TITLES := ["Einstieg","Fortgeschritten","Experte"]
func setup(parent: Control) -> void:
	host = parent
	var tier: int = host.store.data.water_tier
	restore_tier(tier)
	host.audio.set_world("autonomy")
	toolbar = GridContainer.new()
	toolbar.columns = 3
	add_child(toolbar)
	button(toolbar,"⌂ Karte",host.hub)
	button(toolbar,"🔊 Hören",func(): host.narration.play_clip("water_"+str(model.tier)))
	button(toolbar,"★ Stufe",choose)
	board = Board.new()
	board.model = model
	board.reduced_motion = host.store.data.reduced_motion
	add_child(board)
	board.hero.person = host.store.data.hero
	board.watered = completed
	board.was_complete = completed
	board.growth = 1.0 if completed else 0.0
	board.phase = "move"
	board.gesture_done.connect(gesture)
	message = Label.new()
	message.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	message.add_theme_font_size_override("font_size",18)
	board.add_child(message)
	controls = GridContainer.new()
	controls.columns = 3
	add_child(controls)
	mode_button = button(controls,"✋ Legen",toggle_mode)
	water_button = button(controls,"💧 Wasser",turn_water)
	button(controls,"↶ Zurück",func(): model.undo(); changed())
	refresh()
	host.narration.play_clip("water_success" if completed else "water_"+str(model.tier),true)
	var weak_board: WeakRef = weakref(board)
	get_tree().create_timer(1.0).timeout.connect(func():
		var view = weak_board.get_ref()
		if view!=null: view.phase = "idle")
func button(parent: Node,text: String,action: Callable) -> Button:
	var b: Button = host.button(text,action,parent)
	b.add_theme_font_size_override("font_size",18)
	for token in {"🔊":"speaker","💧":"drop","✋":"hand","⌂":"home","↶":"undo"}:
		if text.begins_with(token):
			b.text = text.replace(token,"").strip_edges()
			preload("res://core/modern/icons.gd").apply(b,{"🔊":"speaker","💧":"drop","✋":"hand","⌂":"home","↶":"undo"}[token],24)
			for state in ["normal","hover","pressed","disabled"]:
				var style: StyleBoxFlat = b.get_theme_stylebox(state,"Button").duplicate()
				style.content_margin_left = 4
				style.content_margin_right = 4
				b.add_theme_stylebox_override(state,style)
	return b
func _process(_delta: float) -> void:
	if host==null: return
	position = host.scroll_view.position
	size = host.scroll_view.size
	if size.y<440:
		toolbar.columns = 1;controls.columns = 1
		toolbar.position = Vector2.ZERO;toolbar.size = Vector2(104,216)
		controls.position = Vector2(size.x-104,0);controls.size = Vector2(104,216)
		board.position = Vector2(108,0);board.size = Vector2(size.x-216,size.y)
	else:
		toolbar.columns = 3;controls.columns = 3
		toolbar.position = Vector2.ZERO;toolbar.size = Vector2(size.x,72)
		controls.position = Vector2(0,size.y-72);controls.size = Vector2(size.x,72)
		board.position = Vector2(0,76);board.size = Vector2(size.x,size.y-152)
	message.position = Vector2(78,2)
	message.size = Vector2(maxf(100,board.size.x-84),76 if board.size.y>300 else 50)
	message.max_lines_visible = 3 if board.size.y>300 else 2
	message.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
func persist() -> void:
	if host==null: return
	var snapshot: Dictionary = model.snapshot()
	snapshot.proof = proof.duplicate(true)
	host.store.data.water[str(model.tier)] = snapshot
	host.store.data.water_tier = model.tier
	if host.store.persist()!=OK and is_instance_valid(message): message.text = "Speichern fehlgeschlagen."
func _notification(what: int) -> void:
	if what==NOTIFICATION_APPLICATION_PAUSED:
		if is_instance_valid(board): board.gesture.cancel()
		persist()
func gesture(action: Dictionary) -> void:
	if not action.valid: return
	var changed_model := false
	if action.drag:
		changed_model = model.swap(action.from,action.to)
	elif action.from==4:
		turn_water()
		return
	elif move_mode:
		if selected<0:
			if model.fixed.has(action.from) or model.tiles[action.from]==0: return
			selected = action.from
		else:
			changed_model = model.swap(selected,action.to)
			selected = -1
	else: changed_model = model.rotate(action.from)
	board.selected = selected
	if changed_model: changed()
func toggle_mode() -> void:
	move_mode = not move_mode
	selected = -1
	board.selected = -1
	mode_button.text = "Drehen" if move_mode else "Legen"
	preload("res://core/modern/icons.gd").apply(mode_button,"undo" if move_mode else "hand",24)
func turn_water() -> void:
	model.turn_water()
	changed()
func changed() -> void:
	var r: Dictionary = model.evaluate()
	if r.complete and not completed:
		proof = model.snapshot()
		host.sound(true)
		host.narration.play_clip("water_success",true)
		if not host.store.data.music_locked: host.audio.set_world("success")
	completed = completed or r.complete
	board.phase = "idle" if completed else "think"
	board.watered = completed
	refresh()
	persist()
func refresh() -> void:
	var r: Dictionary = model.evaluate()
	water_button.text = "Stopp" if model.valve else "Wasser"
	var goal: String = ["Versorge die Pflanze.","Pflanze und Vogel haben Durst.","6 Tropfen für beide Pflanzen."][model.tier]
	if completed: goal = "Geschafft! Alles wächst."
	elif model.valve and r.leaks.size()>0: goal = "Hier tropft es. Verbinde die Enden."
	if host.store.data.show_instructions: goal += " Tippe zum Drehen. Ziehe zum Versetzen."
	message.text = goal
	board.queue_redraw()
func choose() -> void:
	if is_instance_valid(choice_panel): return
	board.gesture.cancel()
	choice_panel = PanelContainer.new()
	choice_panel.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(choice_panel)
	var scroll := ScrollContainer.new()
	scroll.follow_focus = true
	choice_panel.add_child(scroll)
	var list := VBoxContainer.new()
	list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(list)
	for i in range(3):
		button(list,["🌱 Einstieg · eine Pflanze","🌿 Fortgeschritten · Vogelbad","🌳 Experte · sechs Tropfen"][i],func(): switch_tier(i))
	button(list,"↻ Neu versuchen",restart)
	button(list,"💡 Hilfe",func(): host.narration.play_clip("water_help"))
	button(list,"Weiter",close_choices)
func close_choices() -> void:
	if is_instance_valid(choice_panel): choice_panel.queue_free();choice_panel = null
func switch_tier(tier: int) -> void:
	persist()
	restore_tier(tier)
	selected = -1
	board.selected = -1
	board.model = model
	board.watered = completed
	board.was_complete = completed
	board.growth = 1.0 if completed else 0.0
	close_choices()
	refresh()
	persist()
	host.narration.play_clip("water_"+str(tier),true)

func restore_tier(tier: int) -> void:
	model.configure(tier)
	var saved = host.store.data.water.get(str(tier),{})
	if model.restore(saved) and model.tier!=tier: model.configure(tier)
	var checked := Model.new()
	var candidate = saved.get("proof",{}) if saved is Dictionary else {}
	proof = checked.snapshot() if checked.restore(candidate) and checked.tier==tier and checked.evaluate().complete else {}
	if model.evaluate().complete: proof = model.snapshot()
	completed = not proof.is_empty()

func restart() -> void:
	model.configure(model.tier)
	proof = {}
	completed = false
	selected = -1
	board.selected = -1
	board.watered = false
	board.was_complete = false
	board.growth = 0
	board.phase = "idle"
	close_choices()
	refresh()
	persist()
	host.narration.play_clip("water_"+str(model.tier),true)
