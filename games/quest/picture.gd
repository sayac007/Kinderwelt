extends Control
const Art = preload("res://core/quest/art.gd")
var task: Dictionary
var marked: Dictionary = {}
var items: Array[Rect2] = []
var hint := false
var host: Control
func _ready() -> void:
	gui_input.connect(input_event)
func symbol(id: String,rect: Rect2,tint := Color.WHITE) -> void:
	Art.object(self,id,rect,tint)
func group(count: int,rect: Rect2,crossed := 0,empty := 0) -> void:
	var columns := mini(5,count)
	var rows := ceili(float(count)/columns)
	var cell := minf(rect.size.x/maxi(columns,1),rect.size.y/maxi(rows,1))
	var origin := rect.get_center()-Vector2(columns*cell,rows*cell)/2
	for i in range(count):
		var box := Rect2(origin+Vector2(i%columns,i/columns)*cell+Vector2.ONE*3,Vector2.ONE*(cell-6))
		items.append(box)
		if i>=count-empty: Art.empty_star(self,box.get_center(),box.size.x*.43)
		else: symbol(task.get("object","star"),box)
		if marked.has(items.size()-1):
			draw_arc(box.get_center(),box.size.x*.49,0,TAU,32,Color("237a79"),3,true)
			Art.text(self,str(marked[items.size()-1]),box.get_center(),20,Color("163e48"))
		if i>=count-crossed:
			draw_line(box.position,box.end,Color("8a4650"),3,true)
			draw_line(Vector2(box.end.x,box.position.y),Vector2(box.position.x,box.end.y),Color("8a4650"),3,true)
func _draw() -> void:
	if task.is_empty(): return
	items.clear()
	var rect := Rect2(Vector2(8,4),size-Vector2(16,8))
	if task.get("kind","")=="dual_pattern":
		var cell: float=rect.size.x/(task.sequence.size()+1)
		var side:=minf(48,cell-8)
		for i in range(task.sequence.size()+1):
			var center:=Vector2(rect.position.x+cell*(i+.5),size.y/2)
			if i<task.sequence.size():
				Art.object(self,task.sequence[i],Rect2(center-Vector2(side/2,side+5),Vector2.ONE*side))
				Art.text(self,str(int(task.counts[i])),center+Vector2(0,22),20)
			else:
				Art.text(self,"?",center-Vector2(0,23),30)
				Art.text(self,"?",center+Vector2(0,22),24)
		return
	if task.has("riddle_scene"):
		preload("res://games/quest/riddle_scene.gd").paint(self,task.riddle_scene,rect)
		Art.text(self,task.get("keyword","?"),Vector2(size.x/2,size.y-12),20)
		return
	if task.has("display"):
		var lines: PackedStringArray=str(task.display).split("\n")
		for i in range(lines.size()):
			var px:=30
			while px>14 and Art.font().get_string_size(lines[i],HORIZONTAL_ALIGNMENT_LEFT,-1,px).x>rect.size.x-8: px-=1
			Art.text(self,lines[i],Vector2(size.x/2,size.y*(i+1)/(lines.size()+1)),px)
		return
	match task.kind:
		"count": group(task.count,rect)
		"add","subtract":
			if task.kind=="subtract": group(task.left,rect,task.right)
			else:
				group(task.left,Rect2(rect.position,Vector2(rect.size.x*.44,rect.size.y)))
				group(task.right,Rect2(Vector2(rect.position.x+rect.size.x*.56,rect.position.y),Vector2(rect.size.x*.44,rect.size.y)))
				Art.text(self,"+",rect.get_center(),30)
		"complete": group(task.right,rect,0,task.right-task.left)
		"initial","rhyme","syllables","word","shadow","discovery":
			var side := minf(size.x*.56,size.y-12)
			var picture := Rect2(rect.get_center()-Vector2.ONE*side/2,Vector2.ONE*side)
			symbol(task.object,picture,Color("283d50") if task.kind=="shadow" else Color.WHITE)
			if hint and task.has("syllables"):
				var parts: Array = task.syllables
				for i in range(parts.size()): Art.text(self,parts[i],Vector2(size.x*(i+1)/(parts.size()+1),size.y-7),20)
		"pattern","sequence","odd":
			var sequence: Array = task.sequence
			var length := sequence.size()+(0 if task.kind=="odd" else 1)
			var cell := minf(68,size.x/mini(length,4))
			var columns := mini(length,4)
			var rows := ceili(float(length)/columns)
			for i in range(length):
				var at := Vector2(size.x*.5+(i%columns-(columns-1)*.5)*cell,size.y*.5+(i/columns-(rows-1)*.5)*cell)
				if i>=sequence.size():
					draw_circle(at,cell*.38,Color("f7e6bd"));Art.text(self,"?",at,32)
				elif sequence[i] is String: symbol(sequence[i],Rect2(at-Vector2.ONE*cell*.42,Vector2.ONE*cell*.84))
				else: Art.text(self,str(int(sequence[i])),at,32)
		"compare":
			group(task.left,Rect2(Vector2.ZERO,Vector2(size.x*.43,size.y)))
			group(task.right,Rect2(Vector2(size.x*.57,0),Vector2(size.x*.43,size.y)))
		"size":
			Art.object(self,"tree",Rect2(Vector2(size.x*.35,8),Vector2(size.x*.3,size.y-16)))
	if hint and not items.is_empty():
		var target: Rect2 = items[0]
		draw_arc(target.get_center(),target.size.x*.55,0,TAU,32,Color("237a79"),4,true)
func input_event(event: InputEvent) -> void:
	var point := Vector2.ZERO
	if event is InputEventScreenTouch and not event.pressed and event.index==0: point=event.position
	elif event is InputEventMouseButton and not event.pressed and event.device!=InputEvent.DEVICE_ID_EMULATION: point=event.position
	else: return
	for i in range(items.size()):
		if items[i].has_point(point):
			if not marked.has(i):
				marked[i] = marked.size()+1
				host.sound()
			queue_redraw()
			accept_event()
			return
