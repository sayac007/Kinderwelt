extends RefCounted
var level: Dictionary
var placements: Array = []
var history: Array = []

static func valid(data: Dictionary) -> bool:
	if not data.get("gaps") is Array or not data.get("pieces") is Array:
		return false
	if data.gaps.is_empty() or data.gaps.size() > 4 or data.pieces.is_empty() or data.pieces.size() > 12:
		return false
	for n in data.gaps + data.pieces:
		if not (n is float or n is int) or n != int(n) or n < 1 or n > 6:
			return false
	return not solution(data).is_empty()

# Independent backtracking over inventory: every piece can be used at most once.
# Surplus pieces are allowed. Return one complete piece->socket assignment.
static func solution(data: Dictionary) -> Array:
	var remaining: Array = data.gaps.duplicate()
	var assignment: Array = []
	assignment.resize(data.pieces.size())
	assignment.fill(-1)
	return assignment if search(data.pieces, remaining, assignment, 0) else []

static func search(pieces: Array, remaining: Array, assignment: Array, index: int) -> bool:
	var done := true
	for n in remaining:
		if n != 0: done = false
	if done: return true
	if index >= pieces.size(): return false
	for slot in range(remaining.size()):
		if remaining[slot] >= pieces[index]:
			remaining[slot] -= pieces[index]
			assignment[index] = slot
			if search(pieces, remaining, assignment, index + 1): return true
			remaining[slot] += pieces[index]
	assignment[index] = -1
	return search(pieces, remaining, assignment, index + 1)

func _init(data: Dictionary) -> void:
	level = data
	placements.resize(level.pieces.size())
	placements.fill(-1)

func filled(slot: int) -> int:
	var total := 0
	for i in range(placements.size()):
		if placements[i] == slot: total += int(level.pieces[i])
	return total

func place(piece: int, slot: int) -> bool:
	if piece < 0 or piece >= placements.size() or slot < 0 or slot >= level.gaps.size(): return false
	if placements[piece] != -1 or filled(slot) + int(level.pieces[piece]) > int(level.gaps[slot]): return false
	placements[piece] = slot
	history.append(piece)
	return true

func undo() -> bool:
	if history.is_empty(): return false
	placements[history.pop_back()] = -1
	return true

func complete() -> bool:
	for slot in range(level.gaps.size()):
		if filled(slot) != int(level.gaps[slot]): return false
	return true

# Find a continuation respecting the child's choices; undo only if stuck.
func next_hint() -> Array:
	var data := {"gaps": [], "pieces": []}
	var available: Array = []
	for slot in range(level.gaps.size()): data.gaps.append(int(level.gaps[slot]) - filled(slot))
	for i in range(placements.size()):
		if placements[i] == -1:
			available.append(i)
			data.pieces.append(level.pieces[i])
	var answer := solution(data)
	if answer.is_empty(): return [-1, -1] # undo, then recalculate
	for i in range(answer.size()):
		if answer[i] >= 0: return [available[i], answer[i]]
	return []
