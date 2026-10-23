extends SceneTree
const Progress = preload("res://games/quest/progress.gd")
const Store = preload("res://core/save_store.gd")
const Tracks = preload("res://core/quest/tracks.gd")
const Wardrobe = preload("res://core/quest/wardrobe.gd")
const Mobile = preload("res://core/mobile.gd")
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
	for dpi in [0.0,160.0,420.0,640.0,1200.0]:
		for pixels in [Vector2i(1080,1920),Vector2i(1080,2400),Vector2i(720,1280)]:
			var portrait:=Mobile.logical_size(pixels,dpi)
			var landscape:=Mobile.logical_size(Vector2i(pixels.y,pixels.x),dpi)
			check(portrait.x>=360 and landscape.y>=360,"Rotation preserves usable short side")
			check(portrait==Vector2i(landscape.y,landscape.x),"Density mapping is symmetric under rotation")
	check(Mobile.safe_insets(Vector2i(1080,2400),Vector2i(360,800),Rect2i(0,0,2400,1080))==Vector4.ZERO,"Ignore stale Android safe-area geometry during rotation")
	check(Mobile.safe_insets(Vector2i(1080,2400),Vector2i(360,800),Rect2i(0,90,1080,2220))==Vector4(0,30,0,30),"Convert valid insets to logical units")
	check(not Progress.same("6",6) and not Progress.same(true,1) and not Progress.same(NAN,NAN),"No coercion of strings, booleans or invalid numbers")
	check(Progress.same(6,6.0),"JSON float and integer answers agree")
	var sanitized:=Store.clean({"hero":"unknown","music_volume":INF,"effects_volume":-99,"voice_auto":"yes","private_name":"discard","stars":9999})
	check(sanitized.hero=="wanja" and sanitized.music_volume==.35 and sanitized.effects_volume==0 and not sanitized.has("private_name") and not sanitized.has("stars"),"Save whitelist rejects unknown/invalid fields")
	check(Store.defaults().hero=="wanja" and preload("res://core/quest/hero.gd").IDS[0]=="wanja","Wanja is the default and first main hero")
	for id in ["wanja","mischa","du","mama","katze","george","squirrel"]:
		check(Store.clean({"hero":id}).hero==id,"All seven family members remain independently selectable and persistent: "+id)
	for pair in [["mina","wanja"],["leo","du"],["sam","mama"],["jule","katze"]]:
		var migrated := Store.clean({"hero":pair[0],"quest":{"solved":{"math_count":true},"hero_chosen":true}})
		check(migrated.hero==pair[1] and migrated.quest.archived.has("math_count") and migrated.quest.hero_chosen,"Replacing a character preserves saved stars and onboarding: "+pair[0])
	check(Store.clean({"music_track":"stars","music_locked":true}).music_track==Tracks.DEFAULT and not Store.clean({"music_track":"stars","music_locked":true}).music_locked,"Unavailable old favourites migrate to an alternating classical playlist")
	check(Tracks.next("moonlight")=="wiener_blut" and Tracks.next("wiener_blut",-1)=="moonlight","Playlist wraps in both directions")
	check(Tracks.next("babbino",1,false,true)=="babbino","Repeat preserves a chosen track")
	for i in range(8): check(Tracks.next("babbino",1,true)!="babbino","Shuffle excludes the current piece")
	# Independently calculated second-round fixtures; first-round rewards migrate separately.
	var expected := {"math_count":11,"math_add":4,"math_take":5,"math_ten":5,"math_compare":16,"math_steps":5,"math_twenty":6,"math_split":2,"german_sun":"SS","german_mouse":"AL","german_apple":"FA","german_rhyme":"MS","german_robot":"FT","german_read":"BP","german_flower":"LV","german_fish":"LC","logic_repeat":8,"logic_triple":9,"logic_odd":"star:9","logic_shadow":"bird","logic_size":12,"logic_double":13,"logic_shape":"sun:10","logic_rule":"bird"}
	var state := Progress.clean({"solved":{"fake":true,"math_count":true,"math_add":false},"subject":"market","hero_chosen":"yes","stars":9999})
	check(state.archived.size()==1 and state.solved.is_empty() and Progress.stars(state)==1,"Only known true completions count; supplied totals are ignored")
	check(state.subject=="math" and not state.hero_chosen,"Invalid subject/hero-chosen types rejected")
	state = Progress.clean(null)
	for subject in Progress.SUBJECTS: check(Progress.tasks(subject).size()==40,"Forty real tasks in "+subject)
	for task in Progress.tasks():
		if expected.has(task.id): check(expected[task.id]==task.answer,"Independent second-round answer fixture "+task.id)
		if task.kind=="add": check(task.answer==task.left+task.right,"Addition is arithmetically correct")
		if task.kind=="subtract": check(task.answer==task.left-task.right,"Subtraction is arithmetically correct")
		if task.kind=="complete": check(task.answer==task.right-task.left,"Complement is arithmetically correct")
		if task.kind=="count": check(task.answer==task.count,"Count is correct")
		check(Progress.correct(task,task.answer),"Accept correct answer")
		for option in task.options:
			if option!=task.answer: check(not Progress.correct(task,option),"Reject distractor "+task.id)
		check(not Progress.correct(task,"forged"),"Reject unknown option")
		check(Progress.award(state,task.id),"First completion earns a star")
		check(not Progress.award(state,task.id),"Repeated completion cannot farm stars")
	check(Progress.stars(state)==320 and not Progress.award(state,"unknown"),"Finite 320-star progression")
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
		check(game.choosing and game.hero_choices.size()==7,"Visible seven-hero first-run choice with Wanja")
		for b in game.hero_choices:
			check(b.get_global_rect().size.x>=64 and b.get_global_rect().size.y>=100,"Large character targets")
			check(Rect2(Vector2.ZERO,logical).encloses(b.get_global_rect()),"Hero choice fits viewport")
		await touch_button(game.hero_choices[3])
		check(app.store.data.hero=="mama" and game.hero_choices[3].get_child(0).reaction>0,"Real touch selects hero and triggers colored reaction")
		await touch_button(game.start_button)
		check(not game.choosing and game.world.hero.person=="mama","Chosen hero enters the playable world")
		for b in game.tabs:
			check(b.size.y>=48 and b.size.x>=64,"Subject touch areas remain usable")
			check(Rect2(Vector2.ZERO,logical).encloses(b.get_global_rect()),"All eight subjects visible without swiping")
		await touch_button(game.tabs[1]);check(game.subject=="german","Deutsch is reachable directly")
		await touch_button(game.tabs[2]);check(game.subject=="logic","Logik is reachable directly")
		await touch_button(game.tabs[0]);check(game.subject=="math","Mathe is reachable directly")
		for index in range(3,8):
			await touch_button(game.tabs[index])
			check(game.subject==Progress.SUBJECTS[index],"Real touch reaches additional subject "+Progress.SUBJECTS[index])
		await touch_button(game.tabs[0])
		var start: float=game.world.hero_x
		await touch(game.world.get_global_rect().position+game.world.station_center(0))
		await create_timer(.85).timeout
		check(game.world.hero_x>start+40 and is_instance_valid(game.task_panel),"Touching station walks character and opens actual task")
		var panel: Control=game.task_panel
		check(panel.heading.get_rect().end.y<panel.picture.position.y,"Instruction does not cover task picture: %s %s %s" % [str(viewport),str(panel.heading.get_rect()),str(panel.picture.position)])
		for b in panel.choices:
			check(b.size.x>=48 and b.size.y>=48,"Answer hit areas at least 48 units")
			check(Rect2(Vector2.ZERO,logical).encloses(b.get_global_rect()),"Answers fit viewport")
		var before := Progress.stars(app.store.data.quest)
		var wrong_index: int=panel.task.options.find_custom(func(option): return not Progress.correct(panel.task,option))
		var correct_index: int=panel.task.options.find(panel.task.answer)
		await touch_button(panel.choices[wrong_index])
		check(not panel.complete and Progress.stars(app.store.data.quest)==before,"Wrong tap retains task and costs nothing")
		await touch_button(panel.choices[correct_index])
		check(panel.complete and Progress.stars(app.store.data.quest)==before+1,"Correct real touch awards exactly one star")
		check(panel.score.points==(before+1)*10 and panel.score.pulse>0,"Task counter is visible and animates a new ten-point award")
		check(panel.heading.text==app.t(panel.praise),"Success has varied visible praise")
		panel.answer(panel.task.answer)
		check(Progress.stars(app.store.data.quest)==before+1,"Repeated touches after success do not award again")
		await touch_button(panel.next_button)
		check(not is_instance_valid(game.task_panel),"Continue returns to walking world")
		var saved := Store.new();saved.load_save()
		check(saved.data.hero=="mama" and saved.data.quest.solved.has("math_count"),"Local hero/progress survive disk roundtrip")
		game._notification(Node.NOTIFICATION_APPLICATION_PAUSED)
		check(not game.world.pressed,"Interruption cancels incomplete gesture")
	# A long character name previously grew the actual Button over the score.
	# Check actual engine rectangles, all names/locales and maximum saved points.
	var saved_progress: Dictionary=app.store.data.quest.duplicate(true)
	for task in Progress.all_tasks():Progress.award(app.store.data.quest,task.id)
	for pixels in [Vector2i(320,568),Vector2i(360,800),Vector2i(800,360),Vector2i(1080,2400),Vector2i(2400,1080)]:
		root.size=pixels;app.simulated_dpi=420 if pixels.x>1000 else 0;app.update_mobile()
		for locale in ["de","en","ru"]:
			app.store.data.locale=locale;app.hub()
			var game: Control=app.game_view
			for id in preload("res://core/quest/hero.gd").IDS:
				app.store.data.hero=id;game.update_score();game.arrange()
				for frame in range(2):await process_frame
				for control in [game.hero_button,game.menu_button,game.title,game.world,game.footer]:
					check(not game.score.get_global_rect().intersects(control.get_global_rect()),"Maximum score does not overlap controls: "+locale+"/"+id+"/"+str(pixels))
				var screen := Vector2(root.content_scale_size if root.content_scale_size.x>0 else pixels)
				check(Rect2(Vector2.ZERO,screen).encloses(game.score.get_global_rect()),"Score stays inside the viewport")
			await touch_button(game.hero_button)
			check(game.choosing,"Figure control stays touchable beside maximum score")
			game.finish_hero()
			await touch_button(game.menu_button)
			check(is_instance_valid(game.menu),"Menu stays touchable beside maximum score")
			game.remove_child(game.menu);game.menu.queue_free();game.menu=null
			game.open_task(0)
			await process_frame
			for control in [game.task_panel.close_button,game.task_panel.speaker,game.task_panel.heading]:
				check(not game.task_panel.score.get_global_rect().intersects(control.get_global_rect()),"Task score does not overlap close, repeat or question")
			game.close_task()
	app.store.data.quest=saved_progress;app.store.data.locale="de";app.hub()
	# Exercise every task through its actual presenter, help, wrong answer and reward.
	for subject in Progress.SUBJECTS:
		game_subject(app,subject)
		var game: Control=app.game_view
		for index in range(Progress.tasks(subject).size()):
			game.open_task(index)
			await process_frame
			var panel: Control=game.task_panel
			panel.help()
			check(panel.picture.hint,"Visual hint exists for every task")
			panel.answer(panel.task.answer)
			check(panel.complete,"Every authored task is completable in presenter")
			game.close_task()
	# All four route pages expose ten tasks, without stale movement on page changes.
	for subject in Progress.SUBJECTS:
		app.game_view.switch_subject(subject)
		for page in range(4):
			app.game_view.world.set_page(page)
			var world: Control=app.game_view.world
			check(world.first_station()==page*10 and world.last_station()==page*10+9,"Every route page has ten reachable stations")
			world.request_station(page*10+9)
			check(world.pending==page*10+9,"Last task on every page is reachable")
			world.set_page(0)
			check(world.pending==-1 and world.target_x==100,"Page change cancels pending arrival")
	for locale in ["de","en","ru"]:
		app.store.data.locale=locale;app.save();app.hub()
		var saved_locale:=Store.new();saved_locale.load_save()
		check(saved_locale.data.locale==locale,"Language persists locally")
		app.store.data.muted=false;app.audio.sync_settings()
		check(app.game_view.title.text==app.t(app.game_view.subject),"Subject caption uses selected language")
		check(app.narration.play_clip("quest/german_sun"),"Localized German instruction loads")
		check(app.narration.queue.is_empty(),"Literacy uses selected language only; no German follow-up")
		app.narration.cancel()
		check(app.narration.queue.is_empty() and not app.audio.music.ducked,"Cancellation clears multilingual queue and ducking")
		app.game_view.switch_subject("geography");app.game_view.open_task(39)
		check(app.game_view.task_panel.heading.text==Progress.tasks("geography")[39].texts[locale].prompt,"Science task uses translated question")
		app.game_view.close_task()
	# Inspect every localized question at the smallest supported portrait size.
	root.content_scale_size=Vector2i.ZERO;root.size=Vector2i(320,568)
	app.simulated_dpi=0;app.update_mobile()
	for locale in ["de","en","ru"]:
		app.store.data.locale=locale;app.store.data.text_scale=1.15;app.hub()
		for subject in Progress.SUBJECTS:
			app.game_view.switch_subject(subject)
			for index in range(40):
				for bonus_index in [-1,0,1]:
					app.game_view.open_task(index)
					if bonus_index>=0:app.game_view.open_bonus(bonus_index)
					await process_frame
					var panel: Control=app.game_view.task_panel
					check(panel.heading.get_line_count()<=panel.heading.max_lines_visible,"Full localized instruction fits: "+locale+"/"+panel.task.id)
					check(panel.heading.get_rect().end.y<panel.picture.position.y and panel.picture.get_rect().end.y<panel.choices[0].position.y if panel.task.kind!="compare" else true,"No heading/picture/answer overlap: "+locale+"/"+panel.task.id)
					app.game_view.close_task()
	app.store.data.text_scale=1.0
	app.store.data.locale="de"
	check(Store.clean({"locale":"xx"}).locale=="de","Unknown locale falls back to German")
	# Reflow one live task across real Window rotations; do not recreate the scene.
	app.store.data.muted=true;app.store.data.locale="ru";app.store.data.text_scale=1.15;app.hub()
	app.store.data.quest.solved.erase("physics_20")
	app.game_view.switch_subject("physics");app.game_view.open_task(19)
	var rotated_panel: Control=app.game_view.task_panel
	var before_rotation:=Progress.stars(app.store.data.quest)
	app.simulated_dpi=420
	for pixels in [Vector2i(1080,2400),Vector2i(2400,1080),Vector2i(1080,2400),Vector2i(1920,1080),Vector2i(1080,1920)]:
		root.size=pixels;app.update_mobile()
		for frame in range(5):await process_frame
		check(app.game_view.task_panel==rotated_panel and not rotated_panel.complete,"Rotation preserves the open task and answer state")
		check(rotated_panel.heading.get_line_count()<=rotated_panel.heading.max_lines_visible,"Rotated question remains fully visible")
		for b in rotated_panel.choices:
			check(Rect2(Vector2.ZERO,Vector2(root.content_scale_size)).encloses(b.get_global_rect()) and b.size.x>=48,"Rotated answers stay on screen and tappable")
		check(rotated_panel.score.get_global_rect().end.y<rotated_panel.heading.get_global_rect().position.y,"Score and question remain separate after rotation")
	await touch_button(rotated_panel.choices[rotated_panel.task.options.find(rotated_panel.task.answer)])
	check(rotated_panel.complete and Progress.stars(app.store.data.quest)==before_rotation+1,"Actual touch solves a task after repeated rotation")
	app.game_view.close_task()
	root.content_scale_size=Vector2i.ZERO;root.size=Vector2i(360,800);app.simulated_dpi=0;app.update_mobile()
	app.store.data.text_scale=1.0;app.store.data.locale="de"
	# New family choices survive selection, disk save and game re-entry.
	for id in ["george","squirrel"]:
		app.game_view.choose_hero()
		var index: int=preload("res://core/quest/hero.gd").IDS.find(id)
		await touch_button(app.game_view.hero_choices[index]);await touch_button(app.game_view.start_button)
		check(app.game_view.world.hero.person==id,"New hero enters actual world: "+id)
		var saved_hero:=Store.new();saved_hero.load_save()
		check(saved_hero.data.hero==id,"New hero persists: "+id)
	# Exercise every real wardrobe button and keep each family member's own look.
	app.store.data.muted=true
	for id in preload("res://core/quest/hero.gd").IDS:
		app.game_view.choose_hero();app.game_view.select_hero(id)
		for index in range(Wardrobe.LOOKS.size()):
			var look: String=Wardrobe.LOOKS[index]
			await touch_button(app.game_view.look_buttons[index])
			check(app.store.data.looks[id]==look,"Native wardrobe selection persists per character: "+id+"/"+look)
			var figure: Control=app.game_view.hero_choices[preload("res://core/quest/hero.gd").IDS.find(id)].get_child(0)
			check(figure.costume==look and ((figure.current_texture() is AtlasTexture)==(look!="classic" or not preload("res://core/quest/cast.gd").FAMILY and id!="squirrel")),"Actual preview uses selected outfit texture")
			for button in app.game_view.look_buttons:
				check(button.size.x>=48 and button.size.y>=48 and Rect2(Vector2.ZERO,Vector2(360,800)).encloses(button.get_global_rect()),"Wardrobe touch targets fit the phone")
		var mask: Image=Wardrobe.mask(id).get_image()
		var data: Dictionary=Wardrobe.catalog.heroes[id]
		for look_index in range(1,5):
			var look: String=Wardrobe.LOOKS[look_index]
			var probe: Array=data.probes[look]
			check(roundi(mask.get_pixel(probe[0],probe[1]).r*255)==look_index,"Native atlas ownership prevents fragments from neighboring outfits")
		app.game_view.finish_hero()
		check(app.game_view.world.hero.costume=="scientist","Walking figure keeps selected clothing")
		app.game_view.open_task(0)
		check(app.game_view.task_panel.companion.costume=="scientist","Success companion keeps selected clothing")
		app.game_view.close_task()
	app.hub()
	check(app.game_view.score.pulse==0 and app.game_view.score.points==Progress.points(app.store.data.quest),"Re-entry shows saved total points without inventing a new award")
	var legacy_cast_save:=Store.clean({"hero":"wanja","looks":{"wanja":"astronaut"},"quest":{"solved":{"math_count":true},"hero_chosen":true}})
	check(legacy_cast_save.hero=="wanja" and legacy_cast_save.looks.wanja=="astronaut" and legacy_cast_save.quest.archived.has("math_count"),"Legacy family IDs, clothing and solved tasks survive either cast variant")
	check(preload("res://core/quest/hero.gd").NAMES.wanja==("Wanja" if preload("res://core/quest/cast.gd").FAMILY else "Nova"),"Selected cast supplies display names independently of saved IDs")
	var wardrobe_save:=Store.new();wardrobe_save.load_save()
	for id in preload("res://core/quest/hero.gd").IDS:check(wardrobe_save.data.looks[id]=="scientist","All seven independent wardrobe choices survive disk roundtrip")
	var invalid_looks:=Store.clean({"scenery":"bad","looks":{"wanja":"fake","george":"hero","intruder":"alien"}})
	check(invalid_looks.scenery=="auto" and invalid_looks.looks.wanja=="classic" and invalid_looks.looks.george=="hero" and not invalid_looks.looks.has("intruder"),"Invalid scenery and clothing data are whitelisted")
	app.store.data.subject_sceneries.math="auto";app.game_view.switch_subject("math")
	for page in range(3):
		app.game_view.world.set_page(page)
		check(app.game_view.world.scene_id()==["mountains","home","castle"][page],"Automatic scenery changes between trail pages")
	for scene in ["mountains","home","castle"]:
		app.store.data.subject_sceneries.math=scene;app.save()
		check(app.game_view.world.scene_id()==scene,"Manual scenery choice overrides the automatic cycle")
	var scenery_save:=Store.new();scenery_save.load_save()
	check(scenery_save.data.subject_sceneries.math=="castle","Manual scenery persists locally")
	app.game_view.world.reduced_motion=false;app.game_view.world.clock=0
	var ghosts: Array=app.game_view.world.ghost_centers()
	app.game_view.world.clock=4
	check(ghosts!=app.game_view.world.ghost_centers(),"Castle ghosts really float with time")
	app.game_view.world.reduced_motion=true;ghosts=app.game_view.world.ghost_centers();app.game_view.world.clock=8
	check(ghosts==app.game_view.world.ghost_centers(),"Reduced motion holds ghosts still")
	app.store.data.subject_sceneries.math="auto"
	var praises: Array=[]
	for n in range(12):praised(app,praises)
	check(praises.slice(0,6).size()==6 and praises[0]==praises[6] and praises[0]!=praises[1],"Six praise variants rotate without immediate repetition")
	app.store.data.muted=false;app.audio.sync_settings()
	# Feedback waits for the entire current utterance instead of swallowing its tail.
	app.narration.play_clip("quest/math_count")
	var spoken: AudioStream=app.narration.stream
	app.narration.speak_feedback("quest/again");app.narration.speak_feedback("quest/praise_2")
	check(app.narration.stream==spoken and app.narration.pending_feedback=="praise_2","Successful feedback replaces pending retry without cutting the question")
	app.narration.stop();app.narration.on_finished()
	check(app.narration.clip=="quest/praise_2" and app.narration.playing,"Finished question starts complete praise")
	app.narration.cancel()
	check(app.narration.pending_feedback.is_empty() and app.narration.queue.is_empty(),"Explicit navigation clears stale queued praise")
	app.musicbox()
	var box: Control=app.body.get_child(0)
	check(box.covers.size()==20,"All twenty classical tracks are selectable")
	for id in preload("res://core/quest/tracks.gd").ITEMS:
		box.select(id)
		check(app.audio.music.world==id and app.audio.music.players[app.audio.music.active].stream!=null,"Track really loads: "+id)
	# Test the actual AudioStreamPlayer.finished path with a short real stream.
	var music: Node = app.audio.music
	var previous: String = music.world
	var short_clip := AudioStreamWAV.new()
	short_clip.format = AudioStreamWAV.FORMAT_16_BITS
	short_clip.mix_rate = 22050
	var silent_samples := PackedByteArray()
	silent_samples.resize(4410)
	short_clip.data = silent_samples
	music.players[music.active].stream=short_clip
	music.players[music.active].play()
	for attempt in range(30):
		if music.world!=previous: break
		await create_timer(.05).timeout
	check(music.world==Tracks.next(previous) and app.store.data.music_track==music.world,"Real audio completion advances and saves the playlist: previous=%s current=%s saved=%s playing=%s" % [previous,music.world,app.store.data.music_track,str(music.players[music.active].playing)])
	check(box.current.text.contains(Tracks.ITEMS[music.world].title),"Music box follows automatic title changes")
	var now: String = music.world
	music.on_finished(1-music.active)
	check(music.world==now,"A stale crossfade player cannot advance the playlist")
	music._notification(Node.NOTIFICATION_APPLICATION_PAUSED)
	music.on_finished(music.active)
	check(music.world==now,"Background suspension cannot consume a track")
	music._notification(Node.NOTIFICATION_APPLICATION_RESUMED)
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

func praised(app: Control,values: Array) -> void:
	values.append(app.praise_id())
