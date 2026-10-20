extends RefCounted
# Shared tap-to-walk / keyboard controller, independent of artwork and puzzle.
var position := Vector2(180, 350)
var target := position
const SPEED := 250.0
const FLOOR := Rect2(60,270,780,220)
func set_target(point: Vector2) -> void:
	target = point.clamp(FLOOR.position,FLOOR.end)
func step(delta: float, axis := Vector2.ZERO) -> void:
	if axis.length_squared()>0:
		set_target(position+axis.normalized()*SPEED*delta)
	position = position.move_toward(target,SPEED*clampf(delta,0,0.1))
func arrived() -> bool:
	return position.distance_to(target)<1
