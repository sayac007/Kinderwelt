extends SceneTree
const Store=preload("res://core/save_store.gd")
const Progress=preload("res://games/quest/progress.gd")
func _initialize() -> void: call_deferred("run")
func run() -> void:
	if OS.get_environment("KINDERWELT_SAVE_TEST")=="write":
		var saved:=Store.new()
		var old_solved: Dictionary={"unknown":true}
		for id in Progress.legacy_rewards():old_solved[id]=true
		saved.data=Store.clean({"schema":4,"quest":{"hero_chosen":true,"solved":old_solved,"total_points":999999999}})
		assert(Progress.points(saved.data.quest)==3200 and saved.data.quest.solved.is_empty())
		assert(Progress.award(saved.data.quest,"math_count"))
		assert(Progress.award(saved.data.quest,"math_count_bonus_1"))
		assert(Progress.award(saved.data.quest,"math_count_bonus_2"))
		assert(not Progress.award(saved.data.quest,"math_count_bonus_2"))
		assert(saved.data.quest.total_points==3360)
		assert(saved.persist()==OK)
		print("SAVE RESTART: migrated all 320 old tasks, earned new 10 + 50 + 100, persisted 3360 points")
	else:
		var app=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
		for frame in range(60): await process_frame
		assert(Progress.points(app.store.data.quest)==3360)
		assert(app.game_view.score.points==3360)
		assert(not app.game_view.choosing)
		assert(not Progress.award(app.store.data.quest,"math_count_bonus_1"))
		assert(Progress.clean(app.store.data.quest).total_points==3360)
		print("SAVE RESTART: new app process restores and displays all 3360 points; no duplicate reward")
		await app.shutdown()
		return
	quit(0)
