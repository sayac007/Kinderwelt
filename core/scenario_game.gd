extends "res://core/learning_game.gd"
const L = preload("res://core/localization.gd")
const ScenarioArt = preload("res://core/scenario_art.gd")
var adult_visible := false
var preview_index := 0
var replaying := false
var story_art: Control

func create_art() -> Control:
	return ScenarioArt.new()

func responsive() -> void:
	for group in layout_grids:
		if is_instance_valid(group): group.columns = 2 if host.size.x < 600 else 3

func chooser() -> void:
	cancel_demonstration()
	index = -1
	wipe()
	art_button({"kind":"home"}, L.message("nav.home"), host.hub)
	text(L.message(entry.name_key))
	text(L.message("common.choose"))
	if levels.is_empty():
		text(L.message("common.unavailable"))
		return
	var group := make_grid()
	for i in range(levels.size()):
		var spec := {"kind":"level", "tier":1, "ordinal":i%3+1}
		if entry.id == "language": spec = {"kind":"story", "card":levels[i].cards[-1]}
		elif entry.id == "autonomy": spec = {"kind":"experiment", "experiment":levels[i].experiment,"values":goal_values(levels[i]),"result":levels[i].goal,"goal":true}
		else: spec = {"kind":"plan", "gives":levels[i].choices[1].gives}
		art_button(spec,L.message(levels[i].title_key),start_level.bind(i),group,Vector2(140,120))
	responsive()

func goal_values(data: Dictionary) -> Array:
	var Experiment = preload("res://games/autonomy/model.gd")
	var limits: Array = Experiment.LIMITS[data.experiment]
	for a in range(limits[0]+1):
		for b in range(limits[1]+1):
			if Experiment.result(data.experiment,[a,b]) == int(data.goal): return [a,b]
	return [0,0]

func start_level(which: int) -> void:
	if which < 0 or which >= levels.size(): return
	adult_visible = false
	preview_index = 0
	super.start_level(which)

func build() -> void:
	wipe()
	var navigation := row()
	art_button({"kind":"home"}, L.message("nav.home"), host.hub,navigation)
	art_button({"kind":"levels"}, L.message("nav.levels"), chooser,navigation)
	art_button({"kind":"retry"}, L.message("nav.retry"),func(): start_level(index),navigation)
	text(L.message(levels[index].title_key))
	var instruction := text(L.message(entry.id+".instruction"))
	instruction.add_theme_font_size_override("font_size",18)
	build_board()
	var controls := row()
	undo_button = art_button({"kind":"undo"},L.message("nav.undo"),undo,controls)
	art_button({"kind":"replay"},L.message("nav.replay"),replay,controls)
	art_button({"kind":"hint","stage":mini(hint_stage,2)},L.message("nav.hint"),hint,controls)
	art_button({"kind":"adult"},L.message("adult.toggle"),toggle_adult)
	if adult_visible:
		text(L.message("adult.intro"))
		text(L.message(levels[index].prompt_key))
	if not feedback.is_empty(): text(L.message(feedback))
	if model.complete():
		text(L.message("common.found"))
		next_button = art_button({"kind":"next"},L.message("nav.next"),next_scenario)
	responsive()

func next_scenario() -> void:
	start_level((index+1)%levels.size())

func toggle_adult() -> void:
	# No password, modal, confirmation, second player or exclusive action.
	adult_visible = not adult_visible
	build()

func finish_if_complete() -> void:
	if model.complete() and not recorded:
		recorded = true
		var progress := Progress.state(host.store,entry.id)
		progress.completed[levels[index].id] = true
		host.store.data.completed[entry.id] = true
		host.save()

func apply_move(_move: Dictionary) -> bool:
	return false

func act(move: Dictionary) -> void:
	cancel_demonstration()
	if not apply_move(move): return
	selected = -1
	gesture = []
	feedback = "" if model.complete() else ("social.observation" if entry.id=="social" else "common.try")
	finish_if_complete()
	host.sound(model.complete())
	build()

func pick(piece: int) -> void:
	cancel_demonstration()
	selected = piece if selected != piece else -1
	gesture = []
	build()
	if not socket_buttons.is_empty(): socket_buttons[0].grab_focus()

func socket(slot: int) -> void:
	if entry.id != "language": return
	if model.placements.find(slot) >= 0:
		act({"action":"remove","target":slot})
	elif selected >= 0:
		act({"action":"place","source":selected,"target":slot})

func undo() -> void:
	cancel_demonstration()
	model.undo()
	selected = -1
	gesture = []
	feedback = ""
	build()

func hint() -> void:
	if demonstrating or index < 0: return
	if model.complete(): return
	assisted = true
	hint_stage = mini(hint_stage+1,3)
	if hint_stage == 1:
		build_hint()
	elif hint_stage == 2:
		apply_move(model.next_hint())
		finish_if_complete()
		build()
	else:
		cancel_demonstration()
		demonstrating = true
		var token := session
		for _step in range(32):
			if model.complete(): break
			build_hint()
			if not host.store.data.reduced_motion:
				await get_tree().create_timer(0.55).timeout
				if not is_inside_tree() or session != token: return
			apply_move(model.next_hint())
			host.sound()
		demonstrating = false
		finish_if_complete()
		build()
	host.sound()

func build_hint() -> void:
	build()
	var move: Dictionary = model.next_hint()
	if move.get("action") == "undo":
		mark(undo_button)
	elif move.get("action") == "place":
		mark(source_buttons[move.source])
		mark(socket_buttons[move.target])
	elif move.get("action") == "set": mark(source_buttons[move.control])
	elif move.get("action") == "test": mark(socket_buttons[0])
	elif move.get("action") == "choose": mark(source_buttons[move.choice])

func mark(button: Button) -> void:
	var art: Control = button.get_child(0)
	art.spec.hint = true
	art.queue_redraw()
	button.grab_focus()

func cancel_demonstration() -> void:
	super.cancel_demonstration()
	replaying = false

func replay() -> void:
	cancel_demonstration()
	if entry.id != "language":
		host.sound()
		return
	replaying = true
	var token := session
	for i in range(levels[index].cards.size()):
		preview_index = i
		if is_instance_valid(story_art):
			story_art.spec.card = levels[index].cards[i]
			story_art.queue_redraw()
		if not host.store.data.muted: host.audio.cue(false,int(levels[index].cards[i].cue))
		await get_tree().create_timer(0.9).timeout
		if not is_inside_tree() or session != token: return
	replaying = false

func preview_step(direction: int) -> void:
	cancel_demonstration()
	preview_index = posmod(preview_index+direction,levels[index].cards.size())
	build()
	if not host.store.data.muted: host.audio.cue(false,int(levels[index].cards[preview_index].cue))
