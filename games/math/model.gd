extends RefCounted
var level: Dictionary
var placements: Array = []
var history: Array = []
var chosen := -1

static func valid(data: Dictionary) -> bool:
	if not data.get("mode") in ["match", "compare", "sort", "share"]: return false
	if data.mode == "compare":
		if not data.get("counts") is Array or data.counts.size() < 2 or data.counts.size() > 3: return false
		var largest := 0
		var maxima := 0
		for n in data.counts:
			if not integer_count(n): return false
			if n > largest:
				largest = int(n)
				maxima = 1
			elif n == largest: maxima += 1
		return maxima == 1
	if not data.get("targets") is Array or not data.get("items") is Array: return false
	if data.targets.is_empty() or data.targets.size() > 3 or data.items.size() > 10: return false
	var needed: Dictionary = {}
	var total := 0
	var kinds: Array = []
	for target in data.targets:
		if not target is Dictionary or not integer_count(target.get("count")): return false
		if not target.get("kind") in ["apple", "pear", "any"]: return false
		total += int(target.count)
		needed[target.kind] = needed.get(target.kind, 0) + int(target.count)
		kinds.append(target.kind)
	if total > data.items.size(): return false
	for item in data.items:
		if not item in ["apple", "pear"]: return false
	for kind in ["apple", "pear"]:
		if data.items.count(kind) < needed.get(kind, 0): return false
	if data.mode == "match" and data.targets.size() != 1: return false
	if data.mode == "sort" and (data.targets.size() != 2 or not "apple" in kinds or not "pear" in kinds): return false
	if data.mode == "share":
		if data.targets.size() < 2: return false
		for target in data.targets:
			if target.kind != "any" or target.count != data.targets[0].count: return false
	return true

static func integer_count(n: Variant) -> bool:
	return (n is float or n is int) and n == int(n) and n >= 1 and n <= 10

func _init(data: Dictionary) -> void:
	level = data
	placements.resize(level.get("items", []).size())
	placements.fill(-1)

func filled(slot: int) -> int:
	return placements.count(slot)

func place(item: int, slot: int) -> bool:
	if level.mode == "compare" or item < 0 or item >= placements.size() or slot < 0 or slot >= level.targets.size(): return false
	var target: Dictionary = level.targets[slot]
	if placements[item] != -1 or filled(slot) >= int(target.count): return false
	if target.kind != "any" and level.items[item] != target.kind: return false
	placements[item] = slot
	history.append(item)
	return true

func choose(slot: int) -> bool:
	if level.mode != "compare" or slot < 0 or slot >= level.counts.size(): return false
	if level.counts[slot] != level.counts.max(): return false
	chosen = slot
	return true

func undo() -> bool:
	if level.mode == "compare":
		chosen = -1
		return true
	if history.is_empty(): return false
	placements[history.pop_back()] = -1
	return true

func complete() -> bool:
	if level.mode == "compare": return chosen >= 0
	for slot in range(level.targets.size()):
		if filled(slot) != int(level.targets[slot].count): return false
	return true

func next_hint() -> Array:
	if complete(): return []
	if level.mode == "compare": return [int(level.counts.find(level.counts.max())), -1]
	for slot in range(level.targets.size()):
		var target: Dictionary = level.targets[slot]
		if filled(slot) >= int(target.count): continue
		for i in range(placements.size()):
			if placements[i] == -1 and (target.kind == "any" or level.items[i] == target.kind): return [i, slot]
	return []
