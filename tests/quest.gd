extends SceneTree
const Progress = preload("res://games/quest/progress.gd")
const Store = preload("res://core/save_store.gd")
var checks := 0
var failures := 0
func check(value: bool,message: String) -> void:
	checks+=1
	if not value: failures+=1;push_error(message)
func _initialize() -> void: call_deferred("run")
func touch(point: Vector2) -> void:
	var e := InputEventScreenTouch.new()
	e.index=0;e.position=root.get_final_transform()*point;e.pressed=true
	Input.parse_input_event(e)
	await process_frame
	e=InputEventScreenTouch.new();e.index=0;e.position=root.get_final_transform()*point
	Input.parse_input_event(e)
	await process_frame
	await process_frame
func touch_button(b: Button) -> void:
	for i in range(3): await process_frame
	await touch(b.get_global_rect().get_center())
func run() -> void:
	check(not Progress.same("6",6) and not Progress.same(true,1) and not Progress.same(NAN,NAN),"No coercion of strings, booleans or invalid numbers")
	check(Progress.same(6,6.0),"JSON float and integer answers agree")
	var sanitized:=Store.clean({"hero":"unknown","music_volume":INF,"effects_volume":-99,"voice_auto":"yes","private_name":"discard","stars":9999})
	check(sanitized.hero=="mina" and sanitized.music_volume==.35 and sanitized.effects_volume==0 and not sanitized.has("private_name") and not sanitized.has("stars"),"Save whitelist rejects unknown/invalid fields")
	var expected := {"math_count":6,"math_add":5,"math_take":4,"math_ten":6,"math_compare":"right","math_steps":8,"math_twenty":14,"math_split":3,"german_sun":"S","german_mouse":"M","german_apple":"A","german_rhyme":"mouse","german_robot":3,"german_read":"BALL","german_flower":2,"german_fish":"F","logic_repeat":"leaf","logic_triple":"moon","logic_odd":"ball","logic_shadow":"tree","logic_size":"large","logic_double":"sun","logic_shape":"robot","logic_rule":"flower"}
	var state := Progress.clean({"solved":{"fake":true,"math_count":true,"math_add":false},"subject":"market","hero_chosen":"yes","stars":9999})
	check(state.solved.size()==1 and Progress.stars(state)==1,"Only known true completions count; supplied totals are ignored")
	check(state.subject=="math" and not state.hero_chosen,"Invalid subject/hero-chosen types rejected")
	state = Progress.clean(null)
	for subject in Progress.SUBJECTS: check(Progress.tasks(subject).size()==8,"Eight real tasks in "+subject)
	for task in Progress.tasks():
		check(expected.has(task.id) and expected[task.id]==task.answer,"Independent authored answer fixture "+task.id)
		check(Progress.correct(task,expected[task.id]),"Accept correct answer")
		for option in task.options:
			if option!=expected[task.id]: check(not Progress.correct(task,option),"Reject distractor "+task.id)
		check(not Progress.correct(task,"forged"),"Reject unknown option")
		check(Progress.award(state,task.id),"First completion earns a star")
		check(not Progress.award(state,task.id),"Repeated completion cannot farm stars")
	check(Progress.stars(state)==24 and not Progress.award(state,"unknown"),"Finite 24-star progression")
	var app: Control = load("res://core/quest/main.tscn").instantiate()
	root.add_child(app)
	app.store.reset();app.store.data.muted=true;app.audio.sync_settings()
	for viewport in [Vector2i(320,568),Vector2i(360,800),Vector2i(800,360),Vector2i(768,1024),Vector2i(1080,2400)]:
		app.simulated_dpi = 420.0 if viewport.x==1080 else 0.0
		root.size = viewport
		app.update_mobile()
		app.store.data.quest=Progress.clean(null);app.hub()
		for i in range(3): await process_frame
		var game: Control=app.game_view
		var logical := Vector2(root.content_scale_size) if root.content_scale_size.x>0 else Vector2(viewport)
		check(game.choosing and game.hero_choices.size()==4,"Visible four-hero first-run choice")
		for b in game.hero_choices:
			check(b.get_global_rect().size.x>=64 and b.get_global_rect().size.y>=100,"Large character targets")
			check(Rect2(Vector2.ZERO,logical).encloses(b.get_global_rect()),"Hero choice fits viewport")
		await touch_button(game.hero_choices[2])
		check(app.store.data.hero=="sam" and game.hero_choices[2].get_child(0).reaction>0,"Real touch selects hero and triggers colored reaction")
		await touch_button(game.start_button)
		check(not game.choosing and game.world.hero.person=="sam","Chosen hero enters the playable world")
		for b in game.tabs: check(b.size.y>=48,"Subject touch areas at least 48 units")
		await touch_button(game.tabs[1]);check(game.subject=="german","Deutsch is reachable directly")
		await touch_button(game.tabs[2]);check(game.subject=="logic","Logik is reachable directly")
		await touch_button(game.tabs[0]);check(game.subject=="math","Mathe is reachable directly")
		var start: float=game.world.hero_x
		await touch(game.world.get_global_rect().position+game.world.station_center(0))
		await create_timer(.85).timeout
		check(game.world.hero_x>start+40 and is_instance_valid(game.task_panel),"Touching station walks character and opens actual task")
		var panel: Control=game.task_panel
		check(panel.heading.get_rect().end.y<panel.picture.position.y,"Instruction does not cover task picture")
		for b in panel.choices:
			check(b.size.x>=48 and b.size.y>=48,"Answer hit areas at least 48 units")
			check(Rect2(Vector2.ZERO,logical).encloses(b.get_global_rect()),"Answers fit viewport")
		var before := Progress.stars(app.store.data.quest)
		await touch_button(panel.choices[0])
		check(not panel.complete and Progress.stars(app.store.data.quest)==before,"Wrong tap retains task and costs nothing")
		await touch_button(panel.choices[1])
		check(panel.complete and Progress.stars(app.store.data.quest)==before+1,"Correct real touch awards exactly one star")
		panel.answer(panel.task.answer)
		check(Progress.stars(app.store.data.quest)==before+1,"Repeated touches after success do not award again")
		await touch_button(panel.next_button)
		check(not is_instance_valid(game.task_panel),"Continue returns to walking world")
		var saved := Store.new();saved.load_save()
		check(saved.data.hero=="sam" and saved.data.quest.solved.has("math_count"),"Local hero/progress survive disk roundtrip")
		game._notification(Node.NOTIFICATION_APPLICATION_PAUSED)
		check(not game.world.pressed,"Interruption cancels incomplete gesture")
	# Exercise every task through its actual presenter, help, wrong answer and reward.
	for subject in Progress.SUBJECTS:
		game_subject(app,subject)
		var game: Control=app.game_view
		for index in range(8):
			game.open_task(index)
			await process_frame
			var panel: Control=game.task_panel
			panel.help()
			check(panel.picture.hint,"Visual hint exists for every task")
			panel.answer(expected[panel.task.id])
			check(panel.complete,"Every authored task is completable in presenter")
			game.close_task()
	app.store.data.muted=false;app.audio.sync_settings()
	app.musicbox()
	var box: Control=app.body.get_child(0)
	check(box.covers.size()==10,"All ten current tracks are selectable")
	for id in preload("res://core/quest/tracks.gd").ITEMS:
		box.select(id)
		check(app.audio.music.players[app.audio.music.active].stream!=null,"Track really loads: "+id)
	box.toggle_favorite()
	var locked: String=app.store.data.music_track
	app.audio.set_world("math")
	check(app.audio.music.world==locked,"Favorite track remains during subject changes")
	for i in range(4): await process_frame
	app.scroll_view.scroll_vertical=300
	await process_frame
	app.settings()
	for i in range(4): await process_frame
	check(app.scroll_view.scroll_vertical==0 and app.body.get_child(0).get_global_rect().position.y>=0,"Opening settings after scrolling music leaves Back visible at the top")
	app.hub()
	check(app.narration.play_clip("quest/german_sun"),"Actual neural offline task audio plays")
	check(app.audio.music.ducked,"Narration ducks music")
	app.narration.cancel()
	check(not app.audio.music.ducked,"Closing narration restores music")
	app.store.data.voice_auto=false
	check(not app.narration.play_clip("quest/german_sun",true),"Autoplay preference respected")
	check(app.narration.play_clip("quest/german_sun"),"Manual repeat still works")
	app.narration.cancel();app.audio.stop();app.audio.music.shutdown()
	await create_timer(.25).timeout
	app.free()
	print("QUEST RESULT: %d checks, %d failures" % [checks,failures])
	quit(1 if failures else 0)
func game_subject(app: Control,subject: String) -> void:
	app.game_view.switch_subject(subject)
