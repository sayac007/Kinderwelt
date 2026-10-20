extends RefCounted
# Transactional gesture: no model edit until release, drift threshold in logical units.
var start := -1
var point := Vector2.ZERO
var current := Vector2.ZERO
var dragging := false
func begin(index: int,at: Vector2) -> void:
	start = index
	point = at
	current = at
	dragging = false
func move(at: Vector2) -> void:
	current = at
	if point.distance_to(at)>=12: dragging = true
func finish(index: int) -> Dictionary:
	var result := {"from":start,"to":index,"drag":dragging,"valid":start>=0 and index>=0}
	cancel()
	return result
func cancel() -> void:
	start = -1
	dragging = false
