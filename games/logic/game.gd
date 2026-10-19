extends "res://core/learning_game.gd"
const Model = preload("res://games/logic/model.gd")

func create_model(data: Dictionary) -> RefCounted:
	return Model.new(data)

func build_board() -> void:
	for slot in range(model.level.gaps.size()):
		var pieces: Array = []
		for i in range(model.placements.size()):
			if model.placements[i] == slot: pieces.append(model.level.pieces[i])
		var show_hint: bool = gesture.size()==2 and gesture[1]==slot
		socket_buttons.append(art_button({"kind":"bridge","target":model.level.gaps[slot],"pieces":pieces,"hint":show_hint,"error":rejected==slot}, "Brückenlücke %d" % [slot+1], socket.bind(slot), self, Vector2(300,104)))
	var inventory := make_grid()
	for i in range(model.level.pieces.size()):
		var show_hint: bool = gesture.size()==2 and gesture[0]==i
		var b := art_button({"kind":"piece","amount":model.level.pieces[i],"selected":selected==i,"hint":show_hint}, "Holzstück mit %d Feldern" % model.level.pieces[i], pick.bind(i), inventory)
		b.disabled = model.placements[i] >= 0
		b.modulate.a = 0.3 if b.disabled else 1.0
		source_buttons.append(b)
