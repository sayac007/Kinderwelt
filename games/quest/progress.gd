extends RefCounted
# Reward state is derived from known, solved tasks, never from supplied totals.
const SUBJECTS := ["math", "german", "logic", "physics", "biology", "chemistry", "body", "geography"]
static var registry: Array = []
static func tasks(subject: String = "") -> Array:
	if registry.is_empty(): registry = JSON.parse_string(FileAccess.get_file_as_string("res://games/quest/tasks.json")).tasks
	return registry if subject.is_empty() else registry.filter(func(t): return t.subject==subject)
static func clean(value: Variant) -> Dictionary:
	var result := {"solved":{}, "subject":"math", "hero_chosen":false}
	if not value is Dictionary: return result
	if value.get("subject") is String and value.subject in SUBJECTS: result.subject = value.subject
	result.hero_chosen = value.get("hero_chosen") is bool and value.hero_chosen
	if value.get("solved") is Dictionary:
		for task in tasks():
			if value.solved.get(task.id) is bool and value.solved[task.id]: result.solved[task.id] = true
	return result
static func award(state: Dictionary,id: String) -> bool:
	if state.solved.has(id) or not tasks().any(func(t): return t.id==id): return false
	state.solved[id] = true
	return true
static func correct(task: Dictionary,value: Variant) -> bool:
	return task.options.any(func(option): return same(option,value)) and same(value,task.answer)
static func same(a: Variant,b: Variant) -> bool:
	if (a is int or a is float) and (b is int or b is float):
		return is_finite(float(a)) and is_finite(float(b)) and float(a)==float(b)
	return a is String and b is String and a==b
static func stars(state: Dictionary) -> int:
	return clean(state).solved.size()
