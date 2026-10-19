extends "res://core/learning_game.gd"
const Model = preload("res://games/math/model.gd")

func create_model(data: Dictionary) -> RefCounted:
	return Model.new(data)

func build_board() -> void:
	if model.level.mode == "compare":
		for slot in range(model.level.counts.size()):
			var count: int = model.level.counts[slot]
			var show_hint: bool = gesture.size()==2 and gesture[0]==slot
			socket_buttons.append(art_button({"kind":"basket","target":count,"amount":count,"selected":model.chosen==slot,"hint":show_hint,"error":rejected==slot}, "Obstkorb auswählen", socket.bind(slot), self, Vector2(280,135)))
		return
	for slot in range(model.level.targets.size()):
		var target: Dictionary = model.level.targets[slot]
		var show_hint: bool = gesture.size()==2 and gesture[1]==slot
		var placed_items: Array = []
		for i in range(model.placements.size()):
			if model.placements[i] == slot: placed_items.append(model.level.items[i])
		var kind: String = target.kind if target.kind != "any" else "apple"
		socket_buttons.append(art_button({"kind":"basket","target":target.count,"amount":model.filled(slot),"items":placed_items,"fruit":kind,"person":model.level.mode=="share","sort":model.level.mode=="sort","hint":show_hint,"error":rejected==slot}, "Obstkorb %d" % [slot+1], socket.bind(slot), self, Vector2(280,135)))
	var inventory := make_grid()
	for i in range(model.level.items.size()):
		var show_hint: bool = gesture.size()==2 and gesture[0]==i
		var b := art_button({"kind":"fruit","fruit":model.level.items[i],"selected":selected==i,"hint":show_hint}, "Apfel" if model.level.items[i]=="apple" else "Birne", pick.bind(i), inventory)
		b.disabled = model.placements[i] >= 0
		b.modulate.a = 0.3 if b.disabled else 1.0
		source_buttons.append(b)
