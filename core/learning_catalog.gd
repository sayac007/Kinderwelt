extends RefCounted
const Bridge = preload("res://games/logic/model.gd")
const Market = preload("res://games/math/model.gd")

static func load_levels(entry: Dictionary) -> Array:
	var parser := JSON.new()
	if parser.parse(FileAccess.get_file_as_string(entry.get("levels", ""))) != OK: return []
	var data = parser.data
	if not data is Dictionary or data.get("schema") != 1 or data.get("module") != entry.id or not data.get("levels") is Array: return []
	return data.levels if valid_levels(entry.id, data.levels) else []

static func valid_levels(module: String, levels: Array) -> bool:
	if module in ["language", "autonomy", "social"]:
		return preload("res://core/scenario_catalog.gd").valid_levels(module, levels)
	if not module in ["logic", "math"] or levels.size() < 9: return false
	var ids: Array = []
	var tiers := [0, 0, 0]
	for item in levels:
		if not item is Dictionary or not item.get("id") is String or item.id.is_empty() or item.id in ids: return false
		var tier = item.get("tier")
		if not (tier is int or tier is float) or tier != int(tier) or tier < 1 or tier > 3: return false
		if not (Bridge.valid(item) if module == "logic" else Market.valid(item)): return false
		ids.append(item.id)
		tiers[int(tier)-1] += 1
	return tiers.min() >= 3
