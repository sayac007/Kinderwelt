extends RefCounted
# Integer port graph, independent of Godot scene/input/audio. N=1 E=2 S=4 W=8.
const DIRS := [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT]
var tier := 0
var rows := 3
var cols := 4
var tiles: Array = []
var fixed := {}
var goals := {}
var budget := 20
var valve := false
var history: Array = []
func _init(which := 0) -> void:
	configure(which)
func configure(which: int) -> void:
	tier = clampi(which,0,2)
	rows = 3 if tier==0 else 4
	tiles = []
	tiles.resize(rows*cols)
	tiles.fill(0)
	fixed = {4:2}
	goals = {7:2} if tier<2 else {3:3,15:3}
	if tier==1: goals[14] = 1
	for index in goals: fixed[index] = 8 if index%cols==3 else 1
	budget = [20,8,6][tier]
	# Initial pieces are deliberately rotated; children can also rearrange them.
	if tier==0:
		tiles[5]=5;tiles[6]=5;tiles[1]=3
	elif tier==1:
		tiles[5]=5;tiles[6]=7;tiles[10]=10;tiles[1]=3
	else:
		tiles[5]=5;tiles[6]=7;tiles[2]=3;tiles[10]=10;tiles[14]=6;tiles[8]=7
	for index in fixed: tiles[index] = fixed[index]
	valve = false
	history.clear()
static func turned(ports: int) -> int:
	return ((ports<<1)&15)|((ports>>3)&1)
func remember() -> void:
	history.append({"tiles":tiles.duplicate(),"valve":valve})
	if history.size()>30: history.pop_front()
func rotate(index: int) -> bool:
	if index<0 or index>=tiles.size() or fixed.has(index) or tiles[index]==0: return false
	remember()
	tiles[index] = turned(tiles[index])
	return true
func swap(a: int,b: int) -> bool:
	if a<0 or b<0 or a>=tiles.size() or b>=tiles.size() or a==b or fixed.has(a) or fixed.has(b) or (tiles[a]==0 and tiles[b]==0): return false
	remember()
	var previous: int = tiles[a]
	tiles[a] = tiles[b]
	tiles[b] = previous
	return true
func turn_water() -> void:
	remember()
	valve = not valve
func undo() -> bool:
	if history.is_empty(): return false
	var old: Dictionary = history.pop_back()
	tiles = old.tiles
	valve = old.valve
	return true
func evaluate(preview := false) -> Dictionary:
	var visited: Array = []
	var leaks: Array = []
	var supplied: Array = []
	if valve or preview: visited.append(4)
	var cursor := 0
	while cursor<visited.size():
		var index: int = visited[cursor]
		cursor += 1
		var at := Vector2i(index%cols,index/cols)
		for direction in range(4):
			if not (int(tiles[index]) & (1<<direction)): continue
			var next: Vector2i = at+DIRS[direction]
			var neighbor := next.y*cols+next.x
			if next.x<0 or next.x>=cols or next.y<0 or next.y>=rows or not (int(tiles[neighbor]) & (1<<((direction+2)%4))):
				leaks.append({"cell":index,"direction":direction})
			elif not visited.has(neighbor): visited.append(neighbor)
	var needed := 0
	for goal in goals:
		needed += goals[goal]
		if visited.has(goal): supplied.append(goal)
	var used := needed+leaks.size()*2
	var complete: bool = (valve or preview) and supplied.size()==goals.size() and used<=budget
	return {"visited":visited,"leaks":leaks,"supplied":supplied,"needed":needed,"used":used,"budget":budget,"complete":complete}
func snapshot() -> Dictionary:
	return {"schema":1,"tier":tier,"tiles":tiles.duplicate(),"valve":valve}
static func shape(ports: int) -> int:
	var smallest := ports
	for i in range(4):
		ports = turned(ports)
		smallest = mini(smallest,ports)
	return smallest
func restore(value: Variant) -> bool:
	if not value is Dictionary or value.get("schema")!=1 or not value.get("valve") is bool: return false
	var level = value.get("tier")
	if not (level is int or level is float) or not is_finite(float(level)) or level!=int(level) or level<0 or level>2: return false
	var fresh = get_script().new(int(level))
	var pieces = value.get("tiles")
	if not pieces is Array or pieces.size()!=fresh.tiles.size(): return false
	var inventory := []
	var expected := []
	for i in range(pieces.size()):
		var piece = pieces[i]
		if not (piece is int or piece is float) or not is_finite(float(piece)) or piece!=int(piece) or piece<0 or piece>15: return false
		if fresh.fixed.has(i):
			if int(piece)!=fresh.fixed[i]: return false
		else:
			inventory.append(shape(int(piece)))
			expected.append(shape(int(fresh.tiles[i])))
	inventory.sort();expected.sort()
	if inventory!=expected: return false
	configure(int(level))
	for i in range(pieces.size()): tiles[i] = int(pieces[i])
	valve = value.valve
	return true
