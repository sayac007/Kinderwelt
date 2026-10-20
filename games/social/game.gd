extends "res://core/scenario_game.gd"
const Model = preload("res://games/social/model.gd")
func create_model(data: Dictionary) -> RefCounted:
	return Model.new(data)

func apply_move(move: Dictionary) -> bool:
	match move.get("action"):
		"choose": return model.choose(move.choice)
		"undo": return model.undo()
	return false

func build_board() -> void:
	var gives: Array = [{},{}] if model.chosen < 0 else model.level.choices[model.chosen].gives
	picture({"kind":"village","people":model.level.people,"gives":gives},160)
	for i in range(model.level.choices.size()):
		var choice: Dictionary = model.level.choices[i]
		source_buttons.append(art_button({"kind":"plan","gives":choice.gives,"style":choice.id,"selected":model.chosen==i},L.message(choice.caption_key),act.bind({"action":"choose","choice":i}),self,Vector2(280,160)))
