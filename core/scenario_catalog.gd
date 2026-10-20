extends RefCounted
const L = preload("res://core/localization.gd")
const Story = preload("res://games/language/model.gd")
const Experiment = preload("res://games/autonomy/model.gd")
const Village = preload("res://games/social/model.gd")

static func valid_levels(module: String, levels: Array) -> bool:
	if module not in ["language", "autonomy", "social"] or levels.size() < 6: return false
	var ids := []
	for item in levels:
		if not item is Dictionary or not item.get("id") is String or item.id.is_empty() or item.id in ids: return false
		ids.append(item.id)
		for field in ["title_key", "prompt_key"]:
			if not item.get(field) is String or not L.has_key(item[field]): return false
		if not item.has("narration") or item.narration != null: return false
		match module:
			"language":
				if not Story.valid(item): return false
				for card in item.cards:
					if not L.has_key(card.caption_key): return false
			"autonomy":
				if not Experiment.valid(item): return false
			"social":
				if not Village.valid(item): return false
				for choice in item.choices:
					if not L.has_key(choice.caption_key): return false
	return true
