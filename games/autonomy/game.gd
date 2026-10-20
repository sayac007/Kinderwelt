extends "res://core/scenario_game.gd"
const Model = preload("res://games/autonomy/model.gd")
func create_model(data: Dictionary) -> RefCounted:
	return Model.new(data)

func apply_move(move: Dictionary) -> bool:
	match move.get("action"):
		"cycle": return model.cycle(move.control)
		"set": return model.set_value(move.control,move.value)
		"test": return model.experiment()
		"undo": return model.undo()
	return false

func build_board() -> void:
	var data: Dictionary = levels[index]
	var goals := {"ramp":"Roll bis zur Fahne auf Feld 4!", "light":"Lenke das Licht auf die Pflanze!", "water":"Bring das Wasser zur Blume!", "wind":"Segle bis zur Fahne auf Feld 4!", "balance":"Mach beide Schalen gleich schwer!", "garden":"Gib der Pflanze Wasser und Sonne!"}
	text(goals[data.experiment])
	picture({"kind":"experiment","experiment":data.experiment,"values":model.values,"result":Model.result(data.experiment,model.values),"target":data.goal},250)
	var settings := make_grid()
	for i in range(2):
		source_buttons.append(art_button({"kind":"setting","experiment":data.experiment,"control":i,"value":model.values[i]},L.message("autonomy.control"),act.bind({"action":"cycle","control":i}),settings,Vector2(140,156)))
	socket_buttons.append(art_button({"kind":"test"},L.message("autonomy.test"),act.bind({"action":"test"})))
	if model.tested:
		text(L.message("autonomy.result"))
