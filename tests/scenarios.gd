extends SceneTree
const Catalog = preload("res://core/catalog.gd")
const Validator = preload("res://core/scenario_catalog.gd")
const Story = preload("res://games/language/model.gd")
const Experiment = preload("res://games/autonomy/model.gd")
const Social = preload("res://games/social/model.gd")
const L = preload("res://core/localization.gd")
const Store = preload("res://core/save_store.gd")
const Progress = preload("res://core/learning_progress.gd")
var checks := 0
var failures := 0
var app: Control

func check(condition: bool, message: String) -> void:
	checks += 1
	if not condition:
		failures += 1
		push_error(message)

func _initialize() -> void:
	call_deferred("run")

func new_model(module: String, data: Dictionary) -> RefCounted:
	if module=="language": return Story.new(data)
	if module=="autonomy": return Experiment.new(data)
	return Social.new(data)

func solve(game: Control) -> void:
	for _step in range(32):
		if game.model.complete(): break
		var move: Dictionary = game.model.next_hint()
		check(not move.is_empty(),"Reachable next move")
		match move.get("action"):
			"place":
				game.source_buttons[move.source].pressed.emit()
				game.socket_buttons[move.target].pressed.emit()
			"set": game.act(move)
			"test": game.socket_buttons[0].pressed.emit()
			"choose": game.source_buttons[move.choice].pressed.emit()
			"undo": game.undo_button.pressed.emit()
			_: break

func run() -> void:
	app = load("res://core/main.tscn").instantiate()
	root.add_child(app)
	await process_frame
	app.store.data = Store.defaults()
	app.store.data.learning = {"math":{"tier":3,"completed":{"previous_market":true},"recent":[]}}
	app.store.data.muted = true
	app.store.data.reduced_motion = true
	var entries := Catalog.modules()
	check(entries.size()==5 and entries.all(func(e): return e.has("runtime")),"All five hub areas have playable runtimes")
	for entry in entries.slice(2):
		var levels := Catalog.levels(entry)
		check(levels.size()>=6 and Validator.valid_levels(entry.id,levels),entry.id+" has six valid scenarios")
		var bad := levels.duplicate(true)
		bad[1].id = bad[0].id
		check(not Validator.valid_levels(entry.id,bad),"Duplicate IDs rejected")
		bad = levels.duplicate(true)
		bad[0].title_key = "missing.translation"
		check(not Validator.valid_levels(entry.id,bad),"Missing localized content rejected")
		for i in range(levels.size()):
			app.open_module(entry)
			var game = app.learning_game
			game.start_level(i)
			game.cancel_demonstration()
			check(not game.model.complete(),"Fresh scenario "+levels[i].id)
			check(not game.adult_visible,"Parent prompts start hidden")
			game.toggle_adult()
			check(game.adult_visible,"Parent prompt is available")
			solve(game)
			check(game.model.complete() and game.recorded,"Solo completion with optional prompt open: "+levels[i].id)
			independent_result(entry.id,game.model)
			var saved := JSON.stringify(app.store.data)
			game.finish_if_complete()
			check(JSON.stringify(app.store.data)==saved,"No duplicate completion/rewards")
			check(Progress.state(app.store,entry.id).completed.has(levels[i].id),"Local per-scenario completion")
			check(Progress.state(app.store,entry.id).tier==1,"New areas do not rank children or raise hidden difficulty")
			game.undo()
			check(not game.model.complete(),"Action is reversible even after completion")
			game.start_level(i)
			game.cancel_demonstration()
			check(game.model.history.is_empty() and not game.recorded and game.hint_stage==0,"Retry clears transient state")
			game.hint()
			check(game.hint_stage==1 and game.model.history.is_empty(),"First hint points without acting")
			game.hint()
			check(game.hint_stage==2 and not game.model.history.is_empty(),"Second hint demonstrates one action")
			if not game.model.complete(): await game.hint()
			check(game.model.complete(),"Worked example can finish every scenario")
			game.next_scenario()
			game.cancel_demonstration()
			check(game.index==(i+1)%levels.size(),"Next scenario remains reachable")
			app.hub()
			check(app.grid.get_child_count()==5,"Hub return remains available")
			await process_frame
		check(Progress.state(app.store,entry.id).completed.size()==levels.size(),"All completions retained")
	await model_cases(entries)
	await input_cases(entries)
	await async_cases(entries)
	check(Progress.state(app.store,"math").tier==3 and Progress.state(app.store,"math").completed.has("previous_market"),"Existing mathematics progress remains intact")
	check(not app.audio.playing,"Muted story cues do not start audio")
	var restored := Store.new()
	restored.load_save()
	for entry in entries.slice(2): check(Progress.state(restored,entry.id).completed.size()==6,"Progress survives reload: "+entry.id)
	check(restored.reset()==OK and not restored.data.has("learning"),"Reset clears scenario progress")
	L.set_locale("en")
	check(L.message("nav.home")=="Zur Kinderwelt","Missing locale falls back to German")
	L.set_locale("de")
	app.audio.stop()
	app.queue_free()
	await create_timer(1.0).timeout
	print("SCENARIOS RESULT: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)

func independent_result(module: String, model: RefCounted) -> void:
	if module=="language":
		var order := []
		order.resize(model.placements.size())
		for i in range(model.placements.size()): order[model.placements[i]]=model.level.cards[i].id
		check(order in model.level.orders,"Actual card order matches an authored story")
	elif module=="autonomy":
		check(model.tested and Experiment.result(model.level.experiment,model.values)==int(model.level.goal),"Experiment actually ran and reached pictured goal")
	else:
		var gives: Array = model.level.choices[model.chosen].gives
		for who in range(2):
			for key in model.level.people[who].needs:
				check(gives[who].get(key,0)>=model.level.people[who].needs[key],"Both characters' authored needs are represented")

func model_cases(entries: Array) -> void:
	for data in Catalog.levels(entries[2]):
		var story := Story.new(data)
		check(not story.place(-1,0) and not story.place(0,99),"Story bounds checked")
		check(not story.remove(-1) and not story.remove(99) and story.history.is_empty(),"Invalid empty slot cannot become a fake removal")
		check(story.place(0,2) and not story.complete(),"Different arrangements are allowed without penalty")
		check(story.remove(2) and story.placements[0]==-1,"Any filled card can be taken back")
		check(story.undo() and story.placements[0]==2,"Removal itself is reversible")
		var bad: Dictionary = data.duplicate(true)
		bad.tray[1]=bad.tray[0]
		check(not Story.valid(bad),"Reject duplicate tray card")
		bad=data.duplicate(true)
		bad.orders[0].pop_back()
		check(not Story.valid(bad),"Reject incomplete story solution")
		# A mistaken early card is recoverable through undo and worked steps.
		app.open_module(entries[2])
		var game = app.learning_game
		game.start_level(Catalog.levels(entries[2]).find(data))
		game.cancel_demonstration()
		game.act({"action":"place","source":0,"target":2})
		solve(game)
		check(game.model.complete(),"Story recovers from out-of-order placement")
	for data in Catalog.levels(entries[3]):
		var experiment := Experiment.new(data)
		check(not experiment.set_value(-1,0) and not experiment.set_value(0,99),"Experiment bounds checked")
		var limits: Array = Experiment.LIMITS[data.experiment]
		var solutions := 0
		for a in range(limits[0]+1):
			for b in range(limits[1]+1):
				var attempt := Experiment.new(data)
				attempt.set_value(0,a)
				attempt.set_value(1,b)
				attempt.experiment()
				if attempt.complete(): solutions+=1
				for step in range(4):
					if attempt.complete(): break
					var move := attempt.next_hint()
					if move.action=="set": attempt.set_value(move.control,move.value)
					else: attempt.experiment()
				check(attempt.complete(),"Every experimental state has a route to goal")
		check(solutions>0,"Experiment has independently enumerated solution")
		var bad: Dictionary = data.duplicate(true)
		bad.goal=99
		check(not Experiment.valid(bad),"Unreachable goal rejected")
	for data in Catalog.levels(entries[4]):
		var scenario := Social.new(data)
		check(not scenario.choose(-1) and not scenario.choose(99),"Social choices have bounds")
		for i in range(data.choices.size()):
			var before := scenario.chosen
			scenario.choose(i)
			check(scenario.chosen==i,"Every idea can be explored without shaming/rejection")
			check(scenario.undo() and scenario.chosen==before,"Every social choice is reversible")
		var bad: Dictionary = data.duplicate(true)
		for choice in bad.choices: choice.gives=[{},{}]
		check(not Social.valid(bad),"Unreachable needs rejected")
		bad=data.duplicate(true)
		bad.choices[0].gives=[{"blocks":6},{"blocks":6}]
		check(not Social.valid(bad),"Overcommitted resources rejected")
	await process_frame

func touch(button: Button) -> void:
	var scroll: Node = app.body.get_parent()
	scroll.ensure_control_visible(button)
	await process_frame
	await process_frame
	var point: Vector2 = root.get_final_transform()*button.get_global_rect().get_center()
	for down in [true,false]:
		var event := InputEventScreenTouch.new()
		event.index=0
		event.position=point
		event.pressed=down
		Input.parse_input_event(event)
		await process_frame
	await process_frame

func input_cases(entries: Array) -> void:
	for entry in entries.slice(2):
		app.open_module(entry)
		var game = app.learning_game
		game.start_level(0)
		game.cancel_demonstration()
		for dimensions in [Vector2i(360,800),Vector2i(1024,600)]:
			root.size=dimensions
			await process_frame
			await process_frame
			check(game.size.x<=dimensions.x+1,"Scenario fits rotated viewport")
			for button in game.source_buttons: check(button.size.x>=96 and button.size.y>=72,"Large child-facing hit targets")
		for step in range(20):
			if game.model.complete(): break
			var move: Dictionary = game.model.next_hint()
			match move.action:
				"place":
					await touch(game.source_buttons[move.source])
					await touch(game.socket_buttons[move.target])
				"set":
					while int(game.model.values[move.control])!=int(move.value): await touch(game.source_buttons[move.control])
				"test": await touch(game.socket_buttons[0])
				"choose": await touch(game.source_buttons[move.choice])
		check(game.model.complete(),"Complete scenario through actual touch dispatch: "+entry.id)
		game.toggle_adult()
		game.undo_button.grab_focus()
		for down in [true,false]:
			var key := InputEventKey.new()
			key.keycode=KEY_ENTER
			key.pressed=down
			root.push_input(key,true)
			await process_frame
		check(not game.model.complete(),"Keyboard undo works with parent prompt open")
		root.size=Vector2i(360,800)
		game.chooser()
		await process_frame
		await process_frame
		check(game.size.x<=361,"All scenario choices fit portrait viewport")
		check(game.index==-1 and game.layout_grids.size()==1,"Self-chosen scenario order remains available")
		app.hub()
		await process_frame

func async_cases(entries: Array) -> void:
	app.store.data.reduced_motion=false
	app.open_module(entries[2])
	var game = app.learning_game
	game.start_level(5)
	check(game.replaying,"Sound-supported story starts a replayable sequence")
	game.start_level(0)
	game.preview_step(1)
	var preview: int = game.preview_index
	await create_timer(1.0).timeout
	check(game.index==0 and game.preview_index==preview,"Manual step cancels old replay callbacks")
	game.hint()
	game.hint()
	game.hint()
	check(game.demonstrating,"Worked example can animate")
	game.start_level(1)
	game.cancel_demonstration()
	await create_timer(0.7).timeout
	check(game.index==1 and game.model.history.is_empty(),"Retry cancels old worked example")
	game.replay()
	app.hub()
	await create_timer(1.0).timeout
	check(app.grid.get_child_count()==5,"Leaving a story safely cancels replay")
	app.store.data.reduced_motion=true
