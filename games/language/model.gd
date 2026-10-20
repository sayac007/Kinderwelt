extends RefCounted
var level: Dictionary
var placements: Array = []
var history: Array = []

func _init(data: Dictionary) -> void:
	level = data
	placements.resize(data.cards.size())
	placements.fill(-1)

static func valid(data: Dictionary) -> bool:
	if not data.get("cards") is Array or data.cards.size() < 3 or data.cards.size() > 5: return false
	if not data.get("tray") is Array or not data.get("orders") is Array or data.orders.is_empty(): return false
	var ids := []
	for card in data.cards:
		if not card is Dictionary or not card.get("id") is String or card.id.is_empty() or card.id in ids: return false
		if not card.get("scene") in ["garden", "bread", "rain", "kite", "paint", "picnic"]: return false
		if not integer(card.get("step"), 0, 4) or not integer(card.get("cue"), 0, 7): return false
		if not card.get("caption_key") is String or not card.has("narration") or card.narration != null: return false
		ids.append(card.id)
	if not permutation(data.tray, ids): return false
	for order in data.orders:
		if not order is Array or not permutation(order, ids): return false
	return true

static func integer(value: Variant, low: int, high: int) -> bool:
	return (value is int or value is float) and is_finite(float(value)) and value == floor(float(value)) and value >= low and value <= high

static func permutation(order: Array, ids: Array) -> bool:
	if order.size() != ids.size(): return false
	var seen := []
	for id in order:
		if not id is String or id not in ids or id in seen: return false
		seen.append(id)
	return true

func place(card: int, slot: int) -> bool:
	if card < 0 or card >= placements.size() or slot < 0 or slot >= placements.size(): return false
	if placements[card] != -1 or slot in placements: return false
	history.append(placements.duplicate())
	placements[card] = slot
	return true

func remove(slot: int) -> bool:
	if slot < 0 or slot >= placements.size(): return false
	var card := placements.find(slot)
	if card == -1: return false
	history.append(placements.duplicate())
	placements[card] = -1
	return true

func undo() -> bool:
	if history.is_empty(): return false
	placements = history.pop_back()
	return true

func continuation(order: Array) -> bool:
	for i in range(placements.size()):
		if placements[i] >= 0 and level.cards[i].id != order[placements[i]]: return false
	return true

func complete() -> bool:
	if -1 in placements: return false
	for order in level.orders:
		if continuation(order): return true
	return false

func next_hint() -> Dictionary:
	if complete(): return {}
	for order in level.orders:
		if not continuation(order): continue
		for slot in range(order.size()):
			if slot in placements: continue
			for i in range(level.cards.size()):
				if level.cards[i].id == order[slot]: return {"action": "place", "source": i, "target": slot}
	return {"action": "undo"}
