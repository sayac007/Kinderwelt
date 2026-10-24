extends SceneTree
# Real Godot lifecycle notifications; this does not simulate Android hardware.
var checks := 0
var failures := 0
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _initialize() -> void:call_deferred("run")
func run() -> void:
	var app: Control=load("res://core/quest/main.tscn").instantiate()
	root.add_child(app)
	app.store.reset();app.store.data.quest.hero_chosen=true
	app.store.data.voice_auto=false;app.store.data.music_volume=.15
	app.audio.sync_settings();app.hub()
	for frame in range(3):await process_frame
	app.game_view.switch_subject("physics");app.game_view.open_task(8)
	app.narration.play_clip("quest/physics_09")
	app.narration.speak_feedback("quest/praise_0")
	app.audio.cue(true)
	app.game_view.world.pressed=true;app.game_view.world.dragging=true
	preload("res://games/quest/progress.gd").award(app.store.data.quest,"physics_09")
	app.store.data.subject_sceneries.physics="moon"
	var position: float = app.narration.get_playback_position()
	app.propagate_notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	check(app.narration.stream_paused,"Background pauses spoken instruction")
	check(app.audio.stream_paused,"Background pauses reward tones")
	check(app.audio.music.suspended,"Background suspends music")
	check(not app.game_view.world.pressed and not app.game_view.world.dragging,"Background cancels held touch gesture")
	check(app.narration.pending_feedback=="praise_0","Background preserves queued praise")
	var restored=preload("res://core/save_store.gd").new();restored.load_save()
	check(restored.data.quest.total_points==10,"Background writes earned score to disk")
	check(restored.data.subject_sceneries.physics=="moon","Background preserves subject scenery")
	await create_timer(.12).timeout
	check(absf(app.narration.get_playback_position()-position)<.10,"Paused instruction does not run silently in background")
	app.propagate_notification(Node.NOTIFICATION_APPLICATION_RESUMED)
	check(not app.narration.stream_paused and not app.audio.stream_paused,"Resume releases speech and effect pause")
	check(not app.audio.music.suspended,"Resume releases music pause")
	check(app.game_view.task_panel.task.id=="physics_09","Resume preserves open challenge")
	for size in [Vector2i(320,568),Vector2i(800,360),Vector2i(360,800),Vector2i(800,360),Vector2i(320,568)]:
		root.size=size;app.update_mobile()
		for frame in range(4):await process_frame
		check(app.game_view.task_panel.task.id=="physics_09","Rotation retains current task")
		check(app.store.data.quest.total_points==10,"Rotation never resets or duplicates points")
		check(app.narration.clip=="quest/physics_09","Rotation does not truncate speech")
		for button in app.game_view.tabs:
			check(button.get_global_rect().size.y>=48,"Rotated subject navigation remains touchable")
	app.narration.cancel();app.audio.stop()
	print("LIFECYCLE: ",checks," checks, ",failures," failures; desktop notifications/resize, no physical Android certification")
	if failures==0:await app.shutdown()
	else:
		app.audio.music.shutdown()
		await create_timer(.25).timeout
		quit(1)
