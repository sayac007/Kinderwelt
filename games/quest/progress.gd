extends RefCounted
# Reward state is derived from known, solved tasks, never from supplied totals.
const SUBJECTS := ["math", "german", "logic", "physics", "biology", "chemistry", "body", "geography"]
static var registry: Array = []
static var legacy_registry: Dictionary = {}
static func legacy_rewards() -> Dictionary:
	if legacy_registry.is_empty(): legacy_registry=JSON.parse_string(FileAccess.get_file_as_string("res://games/quest/legacy-rewards.json")).rewards
	return legacy_registry
static func tasks(subject: String = "") -> Array:
	if registry.is_empty(): registry = JSON.parse_string(FileAccess.get_file_as_string("res://games/quest/tasks.json")).tasks
	return registry if subject.is_empty() else registry.filter(func(t): return t.subject==subject)
static func all_tasks() -> Array:
	var result: Array=[]
	for task in tasks():
		result.append(task)
		result.append_array(task.get("bonuses",[]))
	return result
static func value(id: String) -> int:
	for task in all_tasks():
		if task.id==id: return int(task.get("points",10))
	return 0
static func points(state: Dictionary) -> int:
	var total:=0
	var solved: Dictionary=state.get("solved",{})
	var current: bool=state.get("content_revision",1)==2
	var archived: Dictionary=state.get("archived",{}) if current else solved
	for id in legacy_rewards():
		if archived.get(id) is bool and archived.get(id): total+=int(legacy_rewards()[id])
	if current:
		for task in all_tasks():
			if solved.get(task.id) is bool and solved.get(task.id): total+=int(task.get("points",10))
	return total
static func clean(value: Variant) -> Dictionary:
	var result := {"content_revision":2,"solved":{},"archived":{}, "subject":"math", "hero_chosen":false,"total_points":0}
	if not value is Dictionary: return result
	if value.get("subject") is String and value.subject in SUBJECTS: result.subject = value.subject
	result.hero_chosen = value.get("hero_chosen") is bool and value.hero_chosen
	var old: Variant=value.get("archived") if value.get("content_revision",1)==2 else value.get("solved")
	if old is Dictionary:
		for id in legacy_rewards():
			if old.get(id) is bool and old[id]:result.archived[id]=true
	if value.get("content_revision",1)==2 and value.get("solved") is Dictionary:
		for task in all_tasks():
			if value.solved.get(task.id) is bool and value.solved[task.id]: result.solved[task.id] = true
	result.total_points=points(result)
	return result
static func award(state: Dictionary,id: String) -> bool:
	if state.solved.has(id) or value(id)==0: return false
	state.solved[id] = true
	state.total_points=points(state)
	return true
static func correct(task: Dictionary,value: Variant) -> bool:
	return task.options.any(func(option): return same(option,value)) and task.get("accepted_answers",[task.answer]).any(func(answer): return same(value,answer))
static func same(a: Variant,b: Variant) -> bool:
	if (a is int or a is float) and (b is int or b is float):
		return is_finite(float(a)) and is_finite(float(b)) and float(a)==float(b)
	return a is String and b is String and a==b
static func stars(state: Dictionary) -> int:
	var checked:=clean(state)
	return checked.solved.size()+checked.archived.size()
