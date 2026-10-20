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
	picture({"kind":"experiment","experiment":data.experiment,"values":goal_values(data),"result":data.goal,"goal":true},145)
	var settings := make_grid()
	for i in range(2):
		source_buttons.append(art_button({"kind":"setting","experiment":data.experiment,"control":i,"value":model.values[i]},L.message("autonomy.control"),act.bind({"action":"cycle","control":i}),settings,Vector2(140,120)))
	socket_buttons.append(art_button({"kind":"test"},L.message("autonomy.test"),act.bind({"action":"test"})))
	if model.tested:
		picture({"kind":"experiment","experiment":data.experiment,"values":model.values,"result":Model.result(data.experiment,model.values)},145)
		text(L.message("autonomy.result"))
