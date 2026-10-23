extends SceneTree
const Store=preload("res://core/save_store.gd")
const Progress=preload("res://games/quest/progress.gd")
func _initialize() -> void: call_deferred("run")
func run() -> void:
	if OS.get_environment("KINDERWELT_SAVE_TEST")=="write":
		var saved:=Store.new()
		saved.data=Store.clean({"schema":4,"quest":{"hero_chosen":true,"solved":{"math_count":true,"unknown":true},"total_points":999999999}})
		assert(Progress.points(saved.data.quest)==10)
		assert(Progress.award(saved.data.quest,"math_count_bonus_1"))
		assert(Progress.award(saved.data.quest,"math_count_bonus_2"))
		assert(not Progress.award(saved.data.quest,"math_count_bonus_2"))
		assert(saved.data.quest.total_points==160)
		assert(saved.persist()==OK)
		print("SAVE RESTART: migrated existing score, earned 50 + 100, persisted 160 points")
	else:
		var app=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
		for frame in range(60): await process_frame
		assert(Progress.points(app.store.data.quest)==160)
		assert(app.game_view.score.points==160)
		assert(not app.game_view.choosing)
		assert(not Progress.award(app.store.data.quest,"math_count_bonus_1"))
		assert(Progress.clean(app.store.data.quest).total_points==160)
		print("SAVE RESTART: new app process restores and displays all 160 points; no duplicate reward")
		await app.shutdown()
		return
	quit(0)
