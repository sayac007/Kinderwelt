extends RefCounted
const Numbers = preload("res://games/language/model.gd")
const LIMITS = {"ramp": [3, 1], "light": [2, 1], "water": [2, 1], "wind": [2, 2], "balance": [3, 3], "garden": [2, 2]}
var level: Dictionary
var values: Array = []
var history: Array = []
var tested := false

func _init(data: Dictionary) -> void:
	level = data
	values = data.initial.duplicate()

static func valid(data: Dictionary) -> bool:
	if not LIMITS.has(data.get("experiment", "")) or not data.get("initial") is Array or data.initial.size() != 2: return false
	var limits: Array = LIMITS[data.experiment]
	for i in range(2):
		if not Numbers.integer(data.initial[i], 0, limits[i]): return false
	if not Numbers.integer(data.get("goal"), 0, 6): return false
	for a in range(limits[0] + 1):
		for b in range(limits[1] + 1):
			if result(data.experiment, [a, b]) == int(data.goal): return true
	return false

static func result(experiment: String, state: Array) -> int:
	var a := int(state[0])
	var b := int(state[1])
	match experiment:
		"ramp": return maxi(0, a * 2 - b * 2)
		"light": return 1 if a == 2 and b == 1 else 0
		"water": return 1 if a == 1 and b == 1 else 0
		"wind": return a * b
		"balance": return 1 if a == b and a > 0 else 0
		"garden": return 1 if a == 1 and b >= 1 else 0
	return 0

func set_value(control: int, value: int) -> bool:
	if control < 0 or control >= 2 or value < 0 or value > LIMITS[level.experiment][control]: return false
	if int(values[control]) == value: return false
	history.append({"values": values.duplicate(), "tested": tested})
	values[control] = value
	tested = false
	return true

func cycle(control: int) -> bool:
	if control < 0 or control >= 2: return false
	return set_value(control, (int(values[control]) + 1) % (LIMITS[level.experiment][control] + 1))

func experiment() -> bool:
	if tested: return false
	history.append({"values": values.duplicate(), "tested": tested})
	tested = true
	return true

func undo() -> bool:
	if history.is_empty(): return false
	var previous: Dictionary = history.pop_back()
	values = previous.values
	tested = previous.tested
	return true

func complete() -> bool:
	return tested and result(level.experiment, values) == int(level.goal)

func next_hint() -> Dictionary:
	if complete(): return {}
	var limits: Array = LIMITS[level.experiment]
	# Prefer keeping the child's settings; there can be several valid outcomes.
	var best: Array = []
	var distance := 100
	for a in range(limits[0] + 1):
		for b in range(limits[1] + 1):
			if result(level.experiment, [a, b]) != int(level.goal): continue
			var changes := int(a != int(values[0])) + int(b != int(values[1]))
			if changes < distance:
				distance = changes
				best = [a, b]
	for i in range(2):
		if int(values[i]) != best[i]: return {"action": "set", "control": i, "value": best[i]}
	return {"action": "test"}
