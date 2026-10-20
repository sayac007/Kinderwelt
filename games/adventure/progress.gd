extends RefCounted
const Model = preload("res://games/adventure/power.gd")
var model := Model.new()
var room := 0
var position := Vector2(180,350)
var introduced := false
var proof := {} # Persist a valid solution, not an unverified unlocked flag.
func unlocked() -> bool:
	var check := Model.new()
	return check.restore(proof) and check.difficulty==model.difficulty and check.evaluate().solved
func capture() -> Dictionary:
	return {"schema":1,"puzzle":model.snapshot(),"room":room,"position":[position.x,position.y],"introduced":introduced,"proof":proof.duplicate(true)}
func restore(value: Variant) -> bool:
	if not value is Dictionary or value.get("schema")!=1: return false
	var check := Model.new()
	if not check.restore(value.get("puzzle")): return false
	var location = value.get("room")
	var xy = value.get("position")
	if not (location is int or location is float) or location!=int(location) or location<0 or location>2: return false
	if not xy is Array or xy.size()!=2: return false
	for n in xy:
		if not (n is int or n is float) or not is_finite(float(n)): return false
	if not value.get("introduced") is bool: return false
	var saved_proof := Model.new()
	proof = value.get("proof",{}).duplicate(true) if saved_proof.restore(value.get("proof")) and saved_proof.evaluate().solved else {}
	model = check
	room = int(location) if location!=2 or unlocked() else 1
	position = Vector2(float(xy[0]),float(xy[1])).clamp(Vector2(60,270),Vector2(840,490))
	introduced = value.introduced
	return true
