extends RefCounted
const Numbers = preload("res://games/language/model.gd")
const ICONS = ["quiet", "music", "sun", "shade", "blocks", "tool", "water", "apple", "pear", "space", "play"]
var level: Dictionary
var chosen := -1
var history: Array = []

func _init(data: Dictionary) -> void:
	level = data

static func amounts(value: Variant, empty_allowed := false) -> bool:
	if not value is Dictionary or (value.is_empty() and not empty_allowed) or value.size() > 3: return false
	for key in value:
		if key not in ICONS or not Numbers.integer(value[key], 1, 6): return false
	return true

static func valid(data: Dictionary) -> bool:
	if not data.get("people") is Array or data.people.size() != 2 or not amounts(data.get("stock")): return false
	if not data.get("choices") is Array or data.choices.size() < 2 or data.choices.size() > 4: return false
	for person in data.people:
		if not person is Dictionary or not amounts(person.get("needs")): return false
	var ids := []
	var reachable := false
	for choice in data.choices:
		if not choice is Dictionary or not choice.get("id") is String or choice.id in ids or choice.id.is_empty(): return false
		ids.append(choice.id)
		if not choice.get("caption_key") is String or not choice.get("gives") is Array or choice.gives.size() != 2: return false
		if not choice.has("narration") or choice.narration != null: return false
		var used := {}
		for allocation in choice.gives:
			if not amounts(allocation, true): return false
			for key in allocation: used[key] = used.get(key, 0) + allocation[key]
		for key in used:
			if used[key] > data.stock.get(key, 0): return false
		if fair(data, choice.gives): reachable = true
	return reachable

static func fair(data: Dictionary, gives: Array) -> bool:
	for i in range(2):
		for key in data.people[i].needs:
			if gives[i].get(key, 0) < data.people[i].needs[key]: return false
	return true

func choose(choice: int) -> bool:
	if choice < 0 or choice >= level.choices.size() or choice == chosen: return false
	history.append(chosen)
	chosen = choice
	return true

func undo() -> bool:
	if history.is_empty(): return false
	chosen = history.pop_back()
	return true

func complete() -> bool:
	return chosen >= 0 and fair(level, level.choices[chosen].gives)

func next_hint() -> Dictionary:
	if complete(): return {}
	for i in range(level.choices.size()):
		if fair(level, level.choices[i].gives): return {"action": "choose", "choice": i}
	return {}
