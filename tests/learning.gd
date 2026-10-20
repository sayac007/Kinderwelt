extends SceneTree
const Catalog = preload("res://core/learning_catalog.gd")
const Bridge = preload("res://games/logic/model.gd")
const Market = preload("res://games/math/model.gd")
const Progress = preload("res://core/learning_progress.gd")
const Store = preload("res://core/save_store.gd")
var checks := 0
var failures := 0

func check(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		failures += 1
		push_error(message)

func _initialize() -> void:
	call_deferred("run")

func entries() -> Array:
	return load("res://core/catalog.gd").modules().slice(0,2)

func run() -> void:
	var app = load("res://core/main.tscn").instantiate()
	root.add_child(app)
	await process_frame
	app.store.data.muted = true
	app.store.data.reduced_motion = true
	for entry in entries():
		var levels := Catalog.load_levels(entry)
		check(levels.size()==9, "%s has nine levels" % entry.id)
		var bad := levels.duplicate(true)
		bad[0].tier = 4
		check(not Catalog.valid_levels(entry.id,bad), "Reject invalid tier")
		bad = levels.duplicate(true)
		bad[1].id = bad[0].id
		check(not Catalog.valid_levels(entry.id,bad), "Reject duplicate level ID")
		for data in levels:
			var model = Bridge.new(data) if entry.id=="logic" else Market.new(data)
			check(not model.complete(), data.id+" starts incomplete")
			check(not model.place(-1,0), data.id+" rejects invalid index")
			var steps := 0
			while not model.complete() and steps < 64:
				var move: Array = model.next_hint()
				check(not move.is_empty(), data.id+" has reachable continuation")
				if move.is_empty(): break
				if move==[-1,-1]: model.undo()
				elif data.get("mode")=="compare": check(model.choose(move[0]),data.id+" compare solution")
				else: check(model.place(move[0],move[1]),data.id+" placement accepted")
				steps += 1
			check(model.complete(), data.id+" solo completion")
			model.undo()
			check(not model.complete(), data.id+" undo is reversible after success")
			# Exercise the actual UI contract, every authored task, via Button signals.
			app.open_module(entry)
			var game = app.learning_game
			game.start_level(levels.find(data))
			check(game.hint_stage==0 and not game.assisted,"Fresh hint ladder")
			var initial = game.model.placements.duplicate()
			game.hint()
			check(game.hint_stage==1 and game.assisted,"Gesture is first hint")
			check(game.model.placements==initial,"Gesture does not place items")
			game.hint()
			check(game.hint_stage==2,"Partial step is second hint")
			if not game.model.complete():
				await game.hint()
				check(game.hint_stage==3 and game.model.complete(),"Worked example completes "+data.id)
			else:
				check(game.hint_stage==2,"Single-choice task completed by partial hint")
			check(game.recorded,"Assisted completion recorded")
			game.start_level(levels.find(data))
			check(not game.model.complete() and game.hint_stage==0,"Retry resets state and hints")
			steps = 0
			while not game.model.complete() and steps < 64:
				var move: Array = game.model.next_hint()
				if move==[-1,-1]: game.undo()
				elif data.get("mode")=="compare": game.socket_buttons[move[0]].pressed.emit()
				else:
					game.source_buttons[move[0]].pressed.emit()
					game.socket_buttons[move[1]].pressed.emit()
				steps += 1
			check(game.model.complete() and not game.assisted,"Unaided UI completion "+data.id)
			# Validate the result independently of complete()/next_hint().
			if entry.id == "logic":
				for slot in range(data.gaps.size()):
					var total := 0
					for i in range(game.model.placements.size()):
						if game.model.placements[i] == slot: total += int(data.pieces[i])
					check(total == int(data.gaps[slot]), "Placed bridge spans the authored gap")
			elif data.mode == "compare":
				var chosen: int = game.model.chosen
				check(data.counts.all(func(amount): return amount <= data.counts[chosen]), "Chosen collection independently has the most fruit")
			else:
				for slot in range(data.targets.size()):
					var fruit: Array = []
					for i in range(game.model.placements.size()):
						if game.model.placements[i] == slot: fruit.append(data.items[i])
					check(fruit.size() == int(data.targets[slot].count), "Basket matches authored quantity")
					check(data.targets[slot].kind == "any" or fruit.all(func(kind): return kind == data.targets[slot].kind), "Basket matches authored fruit shape")
					if data.targets[slot].kind == "any":
						check(game.socket_buttons[slot].get_child(0).spec.get("any_fruit", false), "Shared slots do not falsely require apples")
			var progress: Dictionary = Progress.state(app.store,entry.id)
			check(progress.completed.has(data.id),"Per-level completion saved")
			app.hub()
			check(app.grid.get_child_count()==5,"Hub return from "+data.id)
			await process_frame
	# Every legal first bridge choice can recover with reversible hints.
	for data in Catalog.load_levels(entries()[0]):
		for piece in range(data.pieces.size()):
			for slot in range(data.gaps.size()):
				var attempt := Bridge.new(data)
				if not attempt.place(piece,slot): continue
				for _step in range(64):
					if attempt.complete(): break
					var move: Array = attempt.next_hint()
					if move==[-1,-1]: attempt.undo()
					elif not move.is_empty(): attempt.place(move[0],move[1])
				check(attempt.complete(),"Recover from first move: "+data.id)
	# Branching bridge solutions and dead-end recovery, with no forced failure.
	var alternatives := {"gaps":[2],"pieces":[1,1,2]}
	var a := Bridge.new(alternatives)
	check(a.place(2,0) and a.complete(),"Whole plank solution")
	var b := Bridge.new(alternatives)
	check(b.place(0,0) and b.place(1,0) and b.complete(),"Two small planks alternative")
	var stuck := Bridge.new({"gaps":[3,2],"pieces":[1,2,2]})
	check(stuck.place(0,1),"Child may try a locally fitting plank")
	check(stuck.next_hint()==[-1,-1],"Dead-end hint requests undo")
	stuck.undo()
	check(stuck.next_hint()!=[-1,-1],"Undo restores solvability")
	check(not Bridge.valid({"gaps":[3],"pieces":[2]}),"Reject unsolvable bridge")
	check(not Bridge.valid({"gaps":[1.5],"pieces":[2]}),"Reject fractional bridge")
	check(not Market.valid({"mode":"compare","counts":[2,2]}),"Reject ambiguous comparison")
	check(not Market.valid({"mode":"match","targets":[{"count":3,"kind":"apple"}],"items":["pear","pear","pear"]}),"Reject unsolvable fruit inventory")
	var sort_game := Market.new(Catalog.load_levels(entries()[1])[4])
	check(not sort_game.place(0,0),"Wrong fruit shape leaves board unchanged")
	check(sort_game.history.is_empty(),"No penalty or consumed fruit for mismatch")
	# Adaptive suggestions: distinct unaided successes, no failure penalty.
	var store := Store.new()
	var tasks := Catalog.load_levels(entries()[1])
	Progress.record(store,"math",tasks[0],false)
	Progress.record(store,"math",tasks[0],false)
	check(Progress.state(store,"math").tier==1,"Same level cannot inflate progression")
	Progress.record(store,"math",tasks[1],true)
	check(Progress.state(store,"math").tier==1,"Assisted completion is not unaided")
	Progress.record(store,"math",tasks[2],false)
	check(Progress.state(store,"math").tier==2,"Two distinct unaided successes suggest tier two")
	Progress.record(store,"math",tasks[3],false)
	Progress.record(store,"math",tasks[4],false)
	check(Progress.state(store,"math").tier==3,"Tier three progression")
	check(tasks[Progress.recommend(store,"math",tasks)].tier==3,"Recommendation follows current tier")
	check(store.persist()==OK,"Learning state writes")
	var restored := Store.new()
	restored.load_save()
	check(Progress.state(restored,"math").tier==3,"Adaptive state survives reload")
	check(Progress.state(restored,"logic").tier==1,"Modules progress independently")
	# Explicitly exercise malformed optional progress and old schema-1 saves.
	restored.data.learning.math = {"tier":99}
	check(Progress.state(restored,"math").tier==1,"Malformed optional progress recovers")
	restored.reset()
	check(Progress.state(restored,"math").completed.is_empty(),"Adult reset clears learning state")
	app.audio.stop()
	await create_timer(0.5).timeout
	app.queue_free()
	await process_frame
	print("LEARNING RESULT: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
