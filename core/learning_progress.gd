extends RefCounted
# Optional additive save field: old schema-1 foundation saves remain readable.
static func state(store: RefCounted, module: String) -> Dictionary:
	if not store.data.get("learning") is Dictionary: store.data.learning = {}
	var saved = store.data.learning.get(module)
	if not saved is Dictionary or not saved.get("completed") is Dictionary or not saved.get("recent") is Array or not valid_tier(saved.get("tier")):
		store.data.learning[module] = {"tier": 1, "completed": {}, "recent": []}
	store.data.learning[module].tier = int(store.data.learning[module].tier)
	return store.data.learning[module]

static func record(store: RefCounted, module: String, level: Dictionary, assisted: bool) -> void:
	var progress := state(store, module)
	progress.completed[level.id] = true
	# Replaying the same task never counts as two distinct independent successes.
	var recent: Array = []
	for item in progress.recent:
		if item is Dictionary and item.get("id") != level.id: recent.append(item)
	recent.append({"id": level.id, "tier": int(level.tier), "assisted": assisted})
	while recent.size() > 3: recent.pop_front()
	progress.recent = recent
	var independent := 0
	for item in recent:
		if item.get("tier") == progress.tier and item.get("assisted") == false: independent += 1
	if independent >= 2 and progress.tier < 3: progress.tier += 1
	store.data.completed[module] = true

static func recommend(store: RefCounted, module: String, levels: Array) -> int:
	var progress := state(store, module)
	for i in range(levels.size()):
		if levels[i].tier == progress.tier and not progress.completed.has(levels[i].id): return i
	for i in range(levels.size()):
		if not progress.completed.has(levels[i].id): return i
	return 0

static func valid_tier(value: Variant) -> bool:
	return (value is int or value is float) and value == int(value) and value >= 1 and value <= 3
