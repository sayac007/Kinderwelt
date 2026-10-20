extends "res://core/scenario_game.gd"
const Model = preload("res://games/language/model.gd")
func responsive() -> void:
	if index < 0:
		super.responsive()
		return
	for group in layout_grids:
		if is_instance_valid(group): group.columns = 2 if host.size.x < 600 else 3

func create_model(data: Dictionary) -> RefCounted:
	return Model.new(data)

func apply_move(move: Dictionary) -> bool:
	match move.get("action"):
		"place": return model.place(move.source,move.target)
		"remove": return model.remove(move.target)
		"undo": return model.undo()
	return false

func build_board() -> void:
	story_art = picture({"kind":"story","card":levels[index].cards[preview_index]},220)
	text(L.message(levels[index].cards[preview_index].caption_key))
	var reader := row()
	art_button({"kind":"previous"},L.message("language.previous"),preview_step.bind(-1),reader)
	art_button({"kind":"forward"},L.message("language.forward"),preview_step.bind(1),reader)
	var slots := make_grid()
	for slot in range(model.placements.size()):
		var spec := {"kind":"story_slot","ordinal":slot+1}
		var card: int = model.placements.find(slot)
		if card >= 0: spec.card = model.level.cards[card]
		socket_buttons.append(art_button(spec,L.message("language.slot"),socket.bind(slot),slots,Vector2(140,180)))
	var tray := make_grid()
	source_buttons.resize(model.placements.size())
	for id in model.level.tray:
		for i in range(model.level.cards.size()):
			if model.level.cards[i].id != id: continue
			var b := art_button({"kind":"story","card":model.level.cards[i],"selected":selected==i},L.message(model.level.cards[i].caption_key),pick.bind(i),tray,Vector2(140,180))
			b.disabled = model.placements[i] >= 0
			b.modulate.a = 1.0
			if b.disabled: b.get_child(1).text = "✓ " + b.get_child(1).text
			source_buttons[i] = b
	if -1 not in model.placements and not model.complete(): text(L.message("language.full"))
