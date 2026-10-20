extends SceneTree
const Model = preload("res://games/adventure/power.gd")
const Progress = preload("res://games/adventure/progress.gd")
const Movement = preload("res://games/adventure/movement.gd")
var checks := 0
var failures := 0
func check(condition: bool,message: String) -> void:
	checks += 1
	if not condition:
		failures += 1
		push_error(message)
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	# Exhaust the complete state space; independent numerical safety oracle.
	for difficulty in Model.VARIANTS:
		var solutions := {}
		for bits in range(64):
			var m := Model.new()
			m.difficulty = difficulty
			var index := 0
			for key in ["sun","wind","battery","relay","door","lamp"]:
				if bits & (1<<index): m.toggle(key)
				index += 1
			var r: Dictionary = m.evaluate()
			var power := (8 if bits&1 else 0)+(9 if bits&2 else 0)+(6 if bits&4 else 0)
			var cost := (1 if bits&1 else 0)+(2 if bits&2 else 0)+(3 if bits&4 else 0)
			var heat := (1 if bits&1 else 0)+(3 if bits&2 else 0)
			var demand := (4 if bits&8 else 0)+(8 if bits&16 else 0)+(3 if bits&32 else 0)
			var limits: Dictionary = Model.VARIANTS[difficulty]
			var expected: bool = bits&8 and bits&16 and power>=demand and cost<=limits.budget and heat<=limits.heat and power<=limits.fuse and power-demand<=limits.surplus
			check(r.solved==expected,"Safety/solution oracle %s/%d" % [difficulty,bits])
			check(r.power==power and r.demand==demand and r.cost==cost and r.heat==heat,"Energy accounting")
			var copy := Model.new()
			check(copy.restore(m.snapshot()) and copy.snapshot()==m.snapshot(),"Every legal state roundtrips")
			if r.solved: solutions[bits&7] = true
		check(solutions.size()>=2,"Distinct source strategies in "+difficulty)
		for strategy in [["sun","battery","relay","door"],["wind","battery","relay","door"]]:
			var m := Model.new()
			m.difficulty = difficulty
			for action in strategy: m.toggle(action)
			check(m.evaluate().solved,"Documented solution works: "+difficulty)
	var m := Model.new()
	var before: Dictionary = m.snapshot()
	for bad in [null,[],{}, {"difficulty":"Unknown"}, {"difficulty":"Meister","sources":{"sun":1},"circuits":{} }]:
		check(not m.restore(bad) and m.snapshot()==before,"Bad states are rejected transactionally")
	check(not m.toggle("unknown") and m.snapshot()==before,"Unknown control cannot mutate state")
	for key in ["sun","wind","battery"]: m.toggle(key)
	check(not m.evaluate().safe and not m.evaluate().solved,"Excess resources trip protection")
	var p := Progress.new()
	for bad in [null,[],{}, {"schema":1,"puzzle":before,"room":99,"position":[0,0],"introduced":true}]:
		check(not p.restore(bad),"Invalid progress rejected")
	p.room = 2
	var snapshot: Dictionary = p.capture()
	var restored := Progress.new()
	check(restored.restore(snapshot) and restored.room==1 and not restored.unlocked(),"Forged room cannot bypass gate")
	for key in ["sun","battery","relay","door"]: p.model.toggle(key)
	p.proof = p.model.snapshot()
	check(restored.restore(p.capture()) and restored.room==2 and restored.unlocked(),"Solution proof restores open room")
	var controller := Movement.new()
	controller.set_target(Vector2(20000,-20))
	check(controller.target==Vector2(840,270),"Tap targets clamp to walkable floor")
	var start: Vector2 = controller.position
	controller.step(.05)
	check(controller.position.distance_to(start)<=12.51,"Movement speed bounded")
	for i in range(100): controller.step(.05)
	check(controller.arrived(),"Walk reaches destination")
	var app: Control = load("res://core/main.tscn").instantiate()
	root.add_child(app)
	app.store.reset()
	app.store.data.completed = {"logic":{"sentinel":true}}
	for profile in [Vector2i(320,568),Vector2i(360,800),Vector2i(800,360),Vector2i(768,1024)]:
		root.size = profile
		app.open_adventure()
		await process_frame
		await process_frame
		var game: Control = app.adventure
		check(game.progress.model.difficulty=="Tüftler","Tinkerer is default")
		check(not app.scroll_view.visible and game.world.size.y>0,"World has space and needs no scrolling")
		game.progress.introduced = true
		game.close_dialog()
		await process_frame
		var world: Control = game.world
		var touch := InputEventScreenTouch.new()
		touch.pressed = true
		touch.position = Vector2(60,world.size.y*.8)
		world.point_input(touch)
		check(world.controller.target.y>=270 and world.controller.target.y<=490,"Touch chooses walkable destination")
		game.pause_menu()
		check(world.paused,"Pause stops movement")
		var paused_position: Vector2 = world.controller.position
		world._process(.1)
		check(world.controller.position==paused_position,"Simulation stays paused")
		game.close_dialog()
		game.interact("right")
		check(game.progress.room==1,"Connected room entry")
		game.interact("right")
		check(game.progress.room==1,"Locked gate blocks entry")
		game.panel("sources")
		await process_frame
		for key in ["sun","battery"]:
			var b: Button = game.overlay.find_child(key,true,false)
			check(b!=null and b.size.y>=72,"Touchable source button")
			b.pressed.emit()
		for key in ["relay","door"]: game.change(key)
		check(game.progress.unlocked(),"Real panel controls solve mission")
		game.close_dialog()
		game.interact("right")
		check(game.progress.room==2,"Solved gate opens reward room")
		game.set_track("adventure_stars")
		check(app.audio.music.world=="adventure_stars" and app.audio.music.players[app.audio.music.active].stream!=null,"Playable audio selection")
		app.toggle_sound()
		check(not app.audio.music.players[app.audio.music.active].playing,"Global mute stops adventure audio")
		app.toggle_sound()
		game.persist()
		app.hub()
		check(app.scroll_view.visible and app.grid.get_child_count()==5,"Five original worlds preserved")
		app.open_adventure()
		check(app.adventure.progress.room==2 and app.adventure.progress.unlocked(),"Save/relaunch resumes reward room")
		check(app.store.data.completed.logic.sentinel,"Other progress preserved")
		app.adventure.reset_mission("Tüftler")
		app.hub()
		await process_frame
	app.queue_free()
	await process_frame
	print("ADVENTURE RESULT: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
