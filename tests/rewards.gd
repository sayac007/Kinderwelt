extends SceneTree
const Progress=preload("res://games/quest/progress.gd")
const Store=preload("res://core/save_store.gd")
var checks:=0
func check(value: bool,message: String) -> void:
	checks+=1
	assert(value,message)
func _initialize() -> void:call_deferred("run")
func run() -> void:
	var state: Dictionary=Progress.clean({"solved":{"math_count":true,"invalid":true},"total_points":9999999})
	check(state.total_points==10,"Old saves migrate without trusting supplied totals")
	check(Progress.all_tasks().size()==1200,"400 base tasks and 800 independently rewarded bonuses")
	for task in Progress.all_tasks():
		check(Progress.value(task.id)==int(task.points),"Known, bounded reward")
		Progress.award(state,task.id)
	check(Progress.points(state)==64010,"All known base/bonus rewards sum to 64000 plus the archived 10")
	check(Progress.stars(state)==1201,"Bonus achievements survive save sanitisation")
	var app=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
	app.store.reset();app.store.data.quest.hero_chosen=true;app.store.data.muted=true;app.hub()
	await process_frame
	var game: Control=app.game_view
	game.open_task(0)
	game.task_panel.answer(game.task_panel.task.answer)
	check(Progress.points(app.store.data.quest)==10,"Base task awards 10")
	check(game.task_panel.bonus_buttons.size()==2,"Both optional bonuses offered")
	game.task_panel.bonus_buttons[0].pressed.emit()
	check(game.task_panel.bonus_index==0,"50-point bonus can be selected")
	check(game.task_panel.next_button.visible,"Bonus has an immediately available skip")
	game.task_panel.next_button.pressed.emit()
	check(Progress.points(app.store.data.quest)==10,"Skipping neither loses nor invents points")
	game.open_task(0);game.task_panel.answer(game.task_panel.task.answer)
	check(Progress.points(app.store.data.quest)==10,"Reopening a solved parent does not farm points")
	game.task_panel.bonus_buttons[1].pressed.emit()
	var panel: Control=game.task_panel
	panel.answer(panel.task.options.filter(func(v): return not Progress.same(v,panel.task.answer))[0])
	check(Progress.points(app.store.data.quest)==10 and not panel.complete,"Wrong bonus answer has no penalty")
	panel.answer(panel.task.answer)
	check(Progress.points(app.store.data.quest)==110,"100-point bonus is independently selectable")
	check(game.score.points==110 and game.score.reward==100,"World header animates the actual bonus reward")
	var saved:=Store.new();saved.load_save()
	check(Progress.points(saved.data.quest)==110,"Bonus reward is persisted immediately")
	game.close_task()
	for locale in ["de","en","ru"]:
		app.store.data.locale=locale;game.switch_subject("german");game.open_task(0)
		panel=game.task_panel
		check(panel.task.answer=={"de":"SS","en":"SH","ru":"СЫ"}[locale],"New native letter pairs follow the selected alphabet")
		check(panel.task.word=={"de":"SONNENSTRAHL","en":"SUNSHINE","ru":"СОЛНЫШКО"}[locale],"New native vocabulary shown")
		game.close_task()
	var old_solved: Dictionary={}
	for id in Progress.legacy_rewards():old_solved[id]=true
	var graduate: Dictionary=Progress.clean({"solved":old_solved,"total_points":99999999})
	check(Progress.points(graduate)==3200 and graduate.solved.is_empty(),"All old achievements survive but no new task is marked complete")
	for task in Progress.all_tasks():Progress.award(graduate,task.id)
	check(Progress.points(graduate)==67200 and Progress.stars(graduate)==1520,"Lifetime total includes both completed rounds without duplication")
	check(Progress.points(Progress.clean(graduate))==67200,"Cleaning a new-round save does not archive it again")
	app.store.data.locale="ru";game.switch_subject("body");game.open_task(1)
	check(game.task_panel.task.riddle_scene=="sound","Hearing puzzle uses music context, not an ear copy")
	check(game.task_panel.task.keyword=="Слух","Russian keyword uses Cyrillic")
	game.close_task()
	game.switch_subject("logic");game.open_task(2)
	var latin:=RegEx.create_from_string("[A-Za-z]")
	for choice in game.task_panel.choices:
		check(latin.search(choice.tooltip_text)==null,"Russian visual-logic labels never expose encoded Latin object IDs")
	game.close_task()
	var before_restore:=Progress.points(app.store.data.quest)
	app.confirm_old_round()
	app.body.get_child(app.body.get_child_count()-1).pressed.emit()
	check(Progress.points(app.store.data.quest)==before_restore+3200,"Adult-confirmed transfer adds only the previously earned old round")
	check(app.game_view.score.points==before_restore+3200,"Transferred lifetime points are visible immediately")
	app.confirm_old_round()
	app.body.get_child(app.body.get_child_count()-1).pressed.emit()
	check(Progress.points(app.store.data.quest)==before_restore+3200,"Confirmed old-round transfer is idempotent")
	app.narration.cancel();app.audio.music.shutdown();app.audio.stop()
	await create_timer(.15).timeout
	app.free()
	await process_frame
	print("REWARDS: ",checks," checks")
	quit(0)
