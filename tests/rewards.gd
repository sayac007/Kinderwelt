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
	check(Progress.all_tasks().size()==960,"320 base tasks and 640 independently rewarded bonuses")
	for task in Progress.all_tasks():
		check(Progress.value(task.id)==int(task.points),"Known, bounded reward")
		Progress.award(state,task.id)
	check(Progress.points(state)==51200,"All known base/bonus rewards sum to 51200")
	check(Progress.stars(state)==960,"Bonus achievements survive save sanitisation")
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
	var saved:=Store.new();saved.load_save()
	check(Progress.points(saved.data.quest)==110,"Bonus reward is persisted immediately")
	game.close_task()
	for locale in ["de","en","ru"]:
		app.store.data.locale=locale;game.switch_subject("german");game.open_task(0)
		panel=game.task_panel
		var expected: String={"de":"S","en":"S","ru":"С"}[locale]
		check(panel.task.answer==expected,"Native literacy answer follows selected script")
		check(panel.task.word=={"de":"SONNE","en":"SUN","ru":"СОЛНЦЕ"}[locale],"Native literacy word shown")
		game.close_task()
	var syllable_task: Dictionary=preload("res://core/quest/language.gd").task(Progress.tasks("german").filter(func(t): return t.object=="flower" and t.kind=="syllables")[0],"en")
	check(Progress.correct(syllable_task,1) and Progress.correct(syllable_task,2),"English flower accepts both standard syllable counts")
	app.store.data.locale="ru";game.switch_subject("body");game.open_task(1)
	check(game.task_panel.task.riddle_scene=="sound","Hearing puzzle uses music context, not an ear copy")
	check(game.task_panel.task.keyword=="Слух","Russian keyword uses Cyrillic")
	game.close_task()
	app.narration.cancel();app.audio.music.shutdown();app.audio.stop()
	await create_timer(.15).timeout
	app.free()
	await process_frame
	print("REWARDS: ",checks," checks")
	quit(0)
