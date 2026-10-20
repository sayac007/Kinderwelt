extends SceneTree
const Water = preload("res://games/water/model.gd")
const Gesture = preload("res://games/water/gesture.gd")
const Store = preload("res://core/save_store.gd")
const Tracks = preload("res://core/modern/tracks.gd")
var checks := 0
var failures := 0
const SOLUTIONS := [{5:10,6:10},{5:10,6:14,10:5},{5:10,6:13,2:6,10:5,14:3}]
func check(value: bool,message: String) -> void:
	checks += 1
	if not value:
		failures += 1
		push_error(message)
func solve(m: RefCounted) -> void:
	for cell in SOLUTIONS[m.tier]:
		for i in range(4):
			if m.tiles[cell]==SOLUTIONS[m.tier][cell]: break
			m.rotate(cell)
func _initialize() -> void: call_deferred("run")
func touch(point: Vector2) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0;event.position = root.get_final_transform()*point;event.pressed = true
	Input.parse_input_event(event)
	await process_frame
	event = InputEventScreenTouch.new()
	event.index = 0;event.position = root.get_final_transform()*point;event.pressed = false
	Input.parse_input_event(event)
	await process_frame
	await process_frame
func touch_button(button: Button) -> void:
	await process_frame
	await process_frame
	var ancestor: Node = button.get_parent()
	while ancestor!=null:
		if ancestor is ScrollContainer: ancestor.ensure_control_visible(button);break
		ancestor = ancestor.get_parent()
	await process_frame
	await process_frame
	await touch(button.get_global_rect().get_center())
func run() -> void:
	Input.set_emulate_touch_from_mouse(true) # Native Android-style ScrollContainer drag path.
	for tier in range(3):
		var m := Water.new(tier)
		check(not m.evaluate().complete,"Initial puzzle is unsolved")
		solve(m)
		check(not m.evaluate().complete,"Closed tap cannot water plants")
		m.turn_water()
		var r: Dictionary = m.evaluate()
		check(r.complete and r.leaks.is_empty(),"Documented pipe solution: "+str(tier))
		check(r.supplied.size()==m.goals.size(),"Every plant/bath supplied")
		check(r.needed==[2,3,6][tier],"Independent demand fixture")
		for cell in SOLUTIONS[tier]:
			m.rotate(cell)
			check(not m.evaluate().complete,"Broken essential pipe prevents success")
			m.undo()
			check(m.evaluate().complete,"Undo restores working path")
		check(not m.rotate(4) and not m.swap(4,1),"Tap is fixed")
		for goal in m.goals: check(not m.rotate(goal),"Goal cannot be displaced")
		var snapshot: Dictionary = m.snapshot()
		var restored := Water.new()
		check(restored.restore(JSON.parse_string(JSON.stringify(snapshot))) and restored.evaluate().complete,"JSON roundtrip of solved variant")
		var forged: Dictionary = snapshot.duplicate(true)
		forged.tiles[4] = 15
		check(not restored.restore(forged) and restored.evaluate().complete,"Forged source rejected transactionally")
		forged = snapshot.duplicate(true);forged.tiles[0] = 15
		check(not restored.restore(forged),"Cannot create inventory from a save")
		check(not restored.restore({}) and not restored.restore([]),"Malformed save rejected")
		if tier==2:
			check(m.swap(8,5),"Real spare tee can enter the main route")
			for i in range(4):
				if m.tiles[5]==14: break
				m.rotate(5)
			r = m.evaluate()
			check(r.supplied.size()==2 and r.leaks.size()==1,"Both goals reached, but an actual branch leaks")
			check(r.used==8 and r.budget==6 and not r.complete,"Six-drop budget rejects waste")
	var gesture := Gesture.new()
	gesture.begin(5,Vector2.ZERO);gesture.move(Vector2(3,2))
	check(not gesture.finish(5).drag,"Short finger drift stays a tap")
	gesture.begin(5,Vector2.ZERO);gesture.move(Vector2(30,2))
	check(gesture.finish(1).drag,"Long movement becomes a drag")
	gesture.begin(5,Vector2.ZERO)
	check(not gesture.finish(-1).valid,"Release beyond edge cancels")
	var app: Control = load("res://core/main.tscn").instantiate()
	root.add_child(app)
	app.store.reset()
	app.store.data.muted = true
	app.audio.sync_settings()
	for viewport in [Vector2i(320,568),Vector2i(360,800),Vector2i(800,360),Vector2i(768,1024)]:
		root.size = viewport
		app.hub()
		await process_frame
		await process_frame
		check(app.grid.get_child_count()==5,"Five real map places")
		var previous_rects := []
		for b in app.grid.get_children():
			check(b.size.x>=96 and b.size.y>=72,"Map targets are large")
			check(b.position.x>=0 and b.get_rect().end.x<=app.grid.size.x+1,"Map fits width")
			for previous in previous_rects: check(not b.get_rect().intersects(previous),"Map places do not overlap")
			previous_rects.append(b.get_rect())
		if viewport==Vector2i(320,568):
			app.scroll_view.scroll_vertical = 0
			await process_frame
			var start := Vector2(290,420)
			var down := InputEventScreenTouch.new()
			down.index=0;down.position=start;down.pressed=true
			Input.parse_input_event(down)
			await process_frame
			for n in range(6):
				var motion := InputEventScreenDrag.new()
				motion.index=0;motion.position=start+Vector2(0,-25*(n+1));motion.relative=Vector2(0,-25);motion.velocity=Vector2(0,-400)
				Input.parse_input_event(motion)
				await process_frame
			var up := InputEventScreenTouch.new()
			up.index=0;up.position=start+Vector2(0,-150)
			Input.parse_input_event(up)
			await process_frame
			check(app.scroll_view.scroll_vertical>50,"Long synthetic finger swipe actually scrolls the map")
			check(app.active.is_empty(),"Scrolling does not accidentally open a place")
		var catalog = preload("res://core/catalog.gd").modules()
		for i in range(5):
			app.hub()
			await touch_button(app.grid.get_child(i))
			check(app.active.get("id")==catalog[i].id,"Map touch opens existing module %s/%d (actual %s)" % [str(viewport),i,str(app.active.get("id"))])
		app.heroes()
		await process_frame
		var choices: GridContainer = app.body.get_child(2)
		await touch_button(choices.get_child(2))
		check(app.store.data.hero=="sam","Direct hero touch selects Sam")
		var saved := Store.new();saved.load_save()
		check(saved.data.hero=="sam","Hero selection persisted")
		app.open_water()
		await process_frame
		await process_frame
		var game: Control = app.modern_view
		check(game.board.hero.person=="sam","Selected child appears in the mission")
		check(game.board.cell>=48,"Pipe touch area at least 48 logical units")
		game.switch_tier(0)
		game.restart()
		await process_frame
		var before: int = game.model.tiles[5]
		var p: Vector2 = game.board.get_global_transform_with_canvas()*game.board.center(5)
		await touch(p)
		check(game.model.tiles[5]==Water.turned(before),"Viewport touch rotates once")
		var a: int = game.model.tiles[5]
		var b: int = game.model.tiles[1]
		var from: Vector2 = game.board.get_global_transform_with_canvas()*game.board.center(5)
		var to: Vector2 = game.board.get_global_transform_with_canvas()*game.board.center(1)
		var down := InputEventScreenTouch.new()
		down.index = 0;down.position = root.get_final_transform()*from;down.pressed = true
		Input.parse_input_event(down)
		await process_frame
		var drag := InputEventScreenDrag.new()
		drag.index = 0;drag.position = root.get_final_transform()*to;drag.relative = to-from
		Input.parse_input_event(drag)
		await process_frame
		var up := InputEventScreenTouch.new()
		up.index = 0;up.position = root.get_final_transform()*to
		Input.parse_input_event(up)
		await process_frame
		check(game.model.tiles[5]==b and game.model.tiles[1]==a,"Actual drag swaps pipe inventory")
		game._notification(Node.NOTIFICATION_APPLICATION_PAUSED)
		check(game.board.gesture.start==-1,"Interruption cancels unfinished gesture")
		game.persist()
		var expected: Dictionary = game.model.snapshot()
		app.hub();app.open_water()
		check(app.modern_view.model.snapshot()==expected,"Mission resumes exact pipe state")
		for tier in range(3):
			app.modern_view.switch_tier(tier)
			# Fresh fixture for this tier, actions still use the real model.
			app.modern_view.restart()
			check(not app.modern_view.completed,"Restart clears only this mission award")
			solve(app.modern_view.model)
			app.modern_view.turn_water()
			check(app.modern_view.completed,"UI detects success at each difficulty")
			app.modern_view.turn_water()
			check(app.modern_view.completed and app.modern_view.board.watered,"Closing the tap does not undo plant growth")
			app.hub();app.open_water()
			check(app.modern_view.completed and not app.modern_view.model.valve,"Watering achievement resumes with the tap closed")
		app.hub()
		await process_frame
	var closed_state: Dictionary = app.store.data.water["2"].duplicate(true)
	for invalid_proof in [app.store.data.water["0"].proof,{"schema":1}]:
		app.hub()
		app.store.data.water["2"] = closed_state.duplicate(true)
		app.store.data.water["2"].proof = invalid_proof
		app.store.data.water_tier = 2
		app.open_water()
		check(not app.modern_view.completed and not app.modern_view.model.valve,"Invalid or wrong-tier proof cannot award a plant")
	app.store.reset()
	app.musicbox()
	var box: Control = app.body.get_child(0)
	check(Tracks.ITEMS.size()==10 and box.covers.size()==10,"Ten music covers and tracks")
	for id in Tracks.ITEMS:
		box.select(id)
		var stream: AudioStream = app.audio.music.players[app.audio.music.active].stream
		check(stream!=null and stream.get_length()>20,"Playable full-length music: "+id)
		check(app.audio.music.players[app.audio.music.active].playing,"Music starts playing")
	box.select("rain");box.toggle_favorite()
	app.audio.set_world("logic")
	check(app.audio.music.world=="rain","Favorite survives a world change")
	var saved := Store.new();saved.load_save()
	check(saved.data.music_track=="rain" and saved.data.music_locked,"Music preference persisted")
	box.toggle_shuffle()
	var prior: String = box.selected()
	box.step(1)
	check(box.selected()!=prior,"Shuffle chooses a different title")
	box.toggle_favorite()
	box.toggle_shuffle()
	app.audio.set_world("social")
	check(app.audio.music.world=="together","Automatic scene music works")
	app.narration.cancel()
	app.audio.music.sync_settings()
	var normal: float = app.audio.music.players[app.audio.music.active].volume_db
	check(app.narration.play_clip("mina",true),"Bundled German voice actually starts")
	check(app.narration.playing and app.audio.music.ducked,"Speech playback ducks music")
	check(app.audio.music.players[app.audio.music.active].volume_db<=normal-12.9,"Measured music gain lowered by 13 dB")
	var voice_deadline := Time.get_ticks_msec()+int((app.narration.stream.get_length()+1.0)*1000)
	while (app.narration.playing or app.audio.music.ducked) and Time.get_ticks_msec()<voice_deadline:
		await process_frame
	check(not app.narration.playing and not app.audio.music.ducked,"Natural end releases ducking")
	app.store.data.voice_auto = false
	check(not app.narration.play_clip("water_0",true),"Autoplay can be disabled")
	check(app.narration.play_clip("water_0"),"Explicit repeat works with autoplay off")
	app.narration._notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	check(app.narration.stream_paused,"Narration pauses in background")
	app.narration._notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	check(not app.narration.stream_paused,"Narration resumes")
	app.toggle_sound()
	check(not app.narration.playing and not app.audio.music.ducked,"Global mute cancels narration and ducking")
	app.toggle_sound()
	app.store.data.voice_volume = 0
	check(not app.narration.play_clip("water_0"),"Voice volume zero is silent")
	app.store.persist()
	saved.load_save()
	check(not saved.data.voice_auto and saved.data.voice_volume==0,"Voice settings persist")
	app.store.reset()
	app.narration.cancel()
	app.free()
	await create_timer(.5).timeout
	Input.set_emulate_touch_from_mouse(false)
	print("MODERN RESULT: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
