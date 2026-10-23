extends SceneTree
## Exercise the real native-word presenter, including long words and bonus rows.
const Progress = preload("res://games/quest/progress.gd")
const Slots = preload("res://core/quest/letter_slots.gd")
var checks := 0
func check(value: bool,message: String) -> void:
	checks += 1
	assert(value,message)
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var app = load("res://core/quest/main.tscn").instantiate()
	root.add_child(app)
	app.store.reset();app.store.data.muted=true;app.store.data.quest.hero_chosen=true
	app.store.data.text_scale=1.15;app.audio.sync_settings()
	for viewport in [Vector2i(320,568),Vector2i(360,800),Vector2i(800,360),Vector2i(768,1024)]:
		root.content_scale_size=Vector2i.ZERO;root.size=viewport
		app.simulated_dpi=0;app.update_mobile()
		for locale in ["de","en","ru"]:
			app.store.data.locale=locale;app.hub();app.game_view.switch_subject("german")
			for index in range(50):
				for tier in [-1,0,1]:
					app.game_view.open_task(index)
					if tier>=0:app.game_view.open_bonus(tier)
					await process_frame
					var panel: Control=app.game_view.task_panel
					var context: String=locale+"/"+panel.task.id+"/"+str(viewport)
					check(not panel.task.word.to_lower() in panel.heading.text.to_lower(),"No written solution: "+context)
					var previous:=Rect2()
					for button in panel.choices:
						var rect: Rect2=button.get_global_rect()
						check(Rect2(Vector2.ZERO,Vector2(viewport)).encloses(rect),"Letter row stays on screen: "+context)
						check(rect.size.x>=48 and rect.size.y>=48,"Letter row touch size: "+context)
						check(not rect.intersects(previous),"Letter rows do not overlap: "+context)
						previous=rect
						for control in [panel.heading,panel.score,panel.help_button,panel.next_button,panel.feedback]:
							if control.visible:check(not rect.intersects(control.get_global_rect()),"Letter row clear of controls: "+context)
						var visual: Control=button.get_child(0)
						var pattern: String=panel.task.option_displays[str(visual.value)]
						check(visual.slot_pattern==pattern,"Presenter keeps positioned answer: "+context)
						var cells:=Slots.cells(pattern,Rect2(Vector2(9,8),visual.size-Vector2(18,16)))
						check(cells.size()==panel.task.word.length(),"One cell per written position: "+context)
						for cell in cells:check(cell.size.x*.9>=16,"Letters remain readable: "+context)
					app.game_view.close_task()
	print("LETTER LAYOUT: ",checks," checks across 1800 actual word panels")
	await app.shutdown()
