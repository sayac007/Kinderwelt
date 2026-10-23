extends SceneTree
const Store=preload("res://core/save_store.gd")
const Scenery=preload("res://core/quest/scenery.gd")
const Progress=preload("res://games/quest/progress.gd")
var checks:=0
var failures:=0
func check(value: bool,message: String) -> void:
	checks+=1
	if not value:failures+=1;push_error(message)
func _initialize() -> void:call_deferred("run")
func touch(point: Vector2) -> void:
	for pressed in [true,false]:
		var e:=InputEventScreenTouch.new();e.index=0;e.pressed=pressed;e.position=root.get_final_transform()*point
		Input.parse_input_event(e);await process_frame
func run() -> void:
	var regions: Array[Rect2]=[]
	for scene in ["tree","seabed","city","moon"]:
		var region: Rect2=Scenery.region(scene)
		check(Rect2(Vector2.ZERO,Scenery.ATLAS.get_size()).encloses(region),"New background region stays inside the one shared atlas")
		for previous in regions:check(not previous.intersects(region),"World atlas regions never overlap")
		regions.append(region)
	for old in Scenery.CHOICES:
		var data:=Store.clean({"scenery":old,"quest":{"solved":{"math_count":true}},"hero":"mama","looks":{"mama":"alien"}})
		check(data.schema==4 and data.quest.solved.has("math_count") and data.hero=="mama" and data.looks.mama=="alien","Legacy saves retain tasks, characters and clothes")
		for subject in Progress.SUBJECTS:check(data.subject_sceneries[subject]==old,"Migrate global choice into each subject: "+old)
	var invalid:=Store.clean({"subject_sceneries":{"math":"tree","german":12,"logic":"unknown","biology":null,"hacker":"city"}})
	check(invalid.subject_sceneries.math=="tree" and invalid.subject_sceneries.german=="auto" and invalid.subject_sceneries.logic=="auto" and invalid.subject_sceneries.size()==8,"Reject invalid scenery and unknown subjects")
	var independent:=Store.defaults();independent.subject_sceneries.math="moon"
	check(Store.defaults().subject_sceneries.math=="auto","Defaults never share mutable subject settings")
	var app: Control=load("res://core/quest/main.tscn").instantiate();root.add_child(app)
	app.store.reset();app.store.data.muted=true;app.store.data.quest.hero_chosen=true;app.audio.sync_settings();app.hub()
	for profile in [Vector2i(320,568),Vector2i(360,800),Vector2i(800,360),Vector2i(1080,2400)]:
		root.size=profile;app.simulated_dpi=420 if profile.x==1080 else 0;app.update_mobile()
		for scene in Scenery.IDS:
			app.store.data.subject_sceneries.math=scene;app.game_view.switch_subject("math")
			for frame in range(4):await process_frame
			var game: Control=app.game_view
			var world: Control=game.world
			check(world.scene_id()==scene,"Explicit choice survives each device layout")
			# Real touch must move the selected hero and open an actual playable task.
			await touch(world.get_global_rect().position+world.station_center(0))
			await create_timer(.85).timeout
			check(is_instance_valid(game.task_panel) and game.task_panel.task.id=="math_count","Real touch reaches the first task in "+scene+" / "+str(profile))
			if is_instance_valid(game.task_panel):game.close_task()
			# Every task on all pages can be brought into view and reached, with no
			# task ID rewritten by the world type or by vertical camera movement.
			for page in range(4):
				world.set_page(page)
				for index in range(page*10,page*10+10):
					world.hero_x=world.arrival_distance(index);world.target_x=world.hero_x
					world.camera_x=world.follow_camera();world._process(0)
					var c: Vector2=world.station_center(index)
					check(Rect2(38,64,world.size.x-76,world.size.y-102).has_point(c),"Task target remains on screen away from page controls: %s/%s/%d %s" % [profile,scene,index,c])
					world.request_station(index);world._process(0)
					check(is_instance_valid(game.task_panel) and game.task_panel.task.id==Progress.tasks("math")[index].id,"Every station opens its own actual task")
					if is_instance_valid(game.task_panel):game.close_task()
			world.set_page(0)
			var drag:=Vector2(0,100) if scene=="tree" else Vector2(-100,0)
			world.pan_camera(drag)
			check(world.camera_x>0 and world.manual_camera>0,"Pan moves along the world's actual travel axis")
			world.pan_camera(drag*1000)
			check(world.camera_x==world.camera_limit(),"Drag is bounded at the route end")
			world.set_page(1)
			check(world.camera_x==0 and world.pending==-1 and not world.dragging,"Changing page clears stale travel/gestures")
			world.reduced_motion=false;world.clock=0
			var sea: Array=world.marine_centers();world.clock=3
			check(world.marine_centers()!=sea,"Sea creatures have real independent movement")
			world.reduced_motion=true;sea=world.marine_centers();world.clock=9
			check(world.marine_centers()==sea,"Reduced motion stops sea creatures")
			world.set_page(0);world.reduced_motion=false;world.target_x=world.hero_x+100
			world.manual_camera=3
			var before: Vector2=world.path_point(world.hero_x)
			for frame in range(5):world._process(.05)
			if scene=="tree":check(world.path_point(world.hero_x).y<before.y and world.hero.animation=="climb","Tree travel really gains height with climbing animation")
			if scene=="city":
				check(world.vehicle.visible and world.vehicle.phase>0 and world.hero.animation=="drive","City has a moving car with the selected hero as driver")
				check(world.hero.position.y+world.hero.size.y<=world.vehicle.position.y+58 and world.hero.position.y+world.hero.size.y>=world.vehicle.position.y+20,"Car body covers the driver's feet")
			if scene=="seabed":check(world.hero.animation=="swim" and not world.vehicle.visible,"Underwater travel swims instead of driving")
			if scene=="moon":check(world.hero.animation=="moon","Moon travel uses low-gravity hopping")
		app.store.data.subject_sceneries.math="tree";app.store.data.subject_sceneries.german="moon";app.save()
		var saved:=Store.new();saved.load_save()
		check(saved.data.subject_sceneries.math=="tree" and saved.data.subject_sceneries.german=="moon","Different subjects keep independent choices on disk")
		for subject in Progress.SUBJECTS:
			app.game_view.switch_subject(subject)
			var expected: String=app.store.data.subject_sceneries[subject]
			if expected!="auto":check(app.game_view.world.scene_id()==expected,"Subject switch restores its own world")
		app.game_view.switch_subject("math")
		for locale in ["de","en","ru"]:
			app.store.data.locale=locale
			for selected in range(8):
				app.store.data.subject_sceneries.german="seabed"
				app.sceneries()
				for frame in range(4):await process_frame
				check(app.scenery_grid.get_child_count()==8,"All seven worlds and auto have picture buttons in "+locale)
				for card in app.scenery_grid.get_children():
					check(card.get_child(0).get_rect().end.y<=card.size.y-1,"Localized scenery caption fits inside its picture button: "+locale+"/"+card.scenery)
				var choice: Button=app.scenery_grid.get_child(selected)
				check(choice.size.x>=130 and choice.size.y>=138,"Scenery previews have large touch targets")
				app.scroll_view.ensure_control_visible(choice)
				for frame in range(4):await process_frame
				await touch(choice.get_global_rect().get_center())
				check(is_instance_valid(app.game_view) and app.store.data.subject_sceneries.math==Scenery.CHOICES[selected] and app.store.data.subject_sceneries.german=="seabed","Picture selection changes only the current subject: "+Scenery.CHOICES[selected])
				if not is_instance_valid(app.game_view):app.hub()

		app.store.data.locale="de"
	app.narration.cancel();app.audio.music.shutdown();app.audio.stop()
	await create_timer(.2).timeout
	app.free()
	print("WORLD TESTS: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
