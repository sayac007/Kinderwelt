extends Control
const Progress = preload("res://games/quest/progress.gd")
const Art = preload("res://core/quest/art.gd")
const Lang = preload("res://core/quest/language.gd")
const COLORS := {"math":"b75a32","german":"3f7192","logic":"70568b"}
var host: Control
var world: Control
var task_panel: Control
var chooser: Control
var menu: Control
var subject := "math"
var title: Label
var score: Control
var hero_button: Button
var menu_button: Button
var tabs: Array[Button] = []
var footer: Control
var choosing := false
var hero_choices: Array[Button] = []
var start_button: Button
var chooser_label: Label
var look_buttons: Array[Button]=[]
var last_station := 0
func setup(owner_host: Control) -> void:
	host = owner_host
	host.store.data.quest = Progress.clean(host.store.data.get("quest"))
	subject = host.store.data.quest.subject
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	var local_theme := preload("res://core/quest/theme.gd").make_theme()
	local_theme.default_font = Art.font()
	for state in ["normal","hover","pressed","focus","disabled"]:
		var style := StyleBoxFlat.new()
		style.bg_color = Color("fff9eb") if state!="pressed" else Color("e5dfcd")
		style.set_corner_radius_all(30)
		style.border_color = Color("6d7469") if state!="focus" else Color("1b5b79")
		style.set_border_width_all(2 if state!="focus" else 4)
		local_theme.set_stylebox(state,"Button",style)
	theme = local_theme
	hero_button = button(host.t("figure"),choose_hero)
	# Long localized names must not increase Button's minimum width into the score.
	hero_button.clip_text = true
	hero_button.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	hero_button.tooltip_text = host.t("choose_figure")
	menu_button = button("☰",open_menu)
	menu_button.text = ""
	var gear := preload("res://core/quest/icon.gd").new()
	gear.cell = Vector2i(0,1)
	gear.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	menu_button.add_child(gear)
	menu_button.tooltip_text = host.t("menu_tip")
	title = label("")
	score = preload("res://core/quest/score_badge.gd").new()
	score.caption=host.t("points");score.reduced_motion=host.store.data.reduced_motion
	add_child(score)
	footer = Control.new()
	add_child(footer)
	for id in Progress.SUBJECTS:
		var b := button("",func(): switch_subject(id),footer)
		b.tooltip_text = host.t(id)
		var icon := preload("res://core/quest/icon.gd").new()
		if Progress.SUBJECTS.find(id)<3: icon.cell = Vector2i(Progress.SUBJECTS.find(id),0)
		else: icon.object = {"physics":"gear","biology":"leaf","chemistry":"water","body":"heart","geography":"globe"}[id]
		b.add_child(icon)
		var caption := label(host.t(id),b)
		caption.add_theme_font_size_override("font_size",16)
		caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		b.add_theme_font_size_override("font_size",20)
		tabs.append(b)
	resized.connect(arrange)
	switch_subject(subject)
	arrange.call_deferred()
	if not host.store.data.quest.hero_chosen: choose_hero()
func button(caption: String,action: Callable,parent: Node = self) -> Button:
	var b := Button.new()
	b.text = caption
	b.add_theme_font_size_override("font_size",20)
	b.pressed.connect(action)
	parent.add_child(b)
	return b
func label(caption: String,parent: Node = self) -> Label:
	var l := Label.new()
	l.text = caption
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	l.add_theme_font_size_override("font_size",24)
	l.mouse_filter = MOUSE_FILTER_IGNORE
	parent.add_child(l)
	return l
func switch_subject(id: String) -> void:
	if id not in Progress.SUBJECTS: return
	close_task()
	subject = id
	host.store.data.quest.subject = id
	host.save()
	if is_instance_valid(world): remove_child(world);world.queue_free()
	world = preload("res://games/quest/world.gd").new()
	add_child(world)
	move_child(world,0)
	world.setup(host,subject)
	world.station_requested.connect(open_task)
	title.text = host.t(id)
	var done := Progress.tasks(subject).filter(func(t): return host.store.data.quest.solved.has(t.id)).size()
	if done>0 and done<Progress.tasks(subject).size():
		var first: int = Progress.tasks(subject).find_custom(func(t): return not host.store.data.quest.solved.has(t.id))
		world.set_page(first/world.PAGE_SIZE)
		world.hero_x = world.station_x(first)-140
		world.target_x = world.hero_x
		world.camera_x = world.follow_camera()
	world.first_hint = done==0
	host.audio.set_world(id)
	host.narration.play_clip("quest/area_"+id,true)
	if host.store.data.voice_auto and world.scene_id() in ["tree","seabed","city","moon"]:
		host.narration.speak_feedback("quest/world_"+world.scene_id())
	update_score()
	arrange()
func update_score(animate := false) -> void:
	var stars := Progress.stars(host.store.data.quest)
	score.set_total(stars,animate,Progress.points(host.store.data.quest))
	hero_button.text = hero_name(host.store.data.hero)
	hero_button.tooltip_text = host.t("choose_figure")+": "+hero_button.text
	for i in range(tabs.size()):
		var style := StyleBoxFlat.new()
		style.bg_color = Color("fae3b4") if Progress.SUBJECTS[i]==subject else Color("fff8e9")
		style.set_corner_radius_all(25)
		style.set_border_width_all(2)
		style.border_color = Color("c8bda7")
		tabs[i].add_theme_stylebox_override("normal",style)
		tabs[i].get_child(1).add_theme_color_override("font_color",Art.INK)
	queue_redraw()
func arrange() -> void:
	if not is_instance_valid(world): return
	if OS.get_name()=="Android":
		var inset:=preload("res://core/mobile.gd").safe_insets(get_window().size,get_window().content_scale_size,DisplayServer.get_display_safe_area(),get_window().position)
		offset_left=inset.x;offset_top=inset.y;offset_right=-inset.z;offset_bottom=-inset.w
	var landscape := size.x>size.y*1.3
	hero_button.position=Vector2(10,22);hero_button.size=Vector2(83,48)
	menu_button.position=Vector2(size.x-60,22);menu_button.size=Vector2(50,48)
	title.position=Vector2(96,0);title.size=Vector2(size.x-159,31)
	title.add_theme_font_size_override("font_size",20)
	score.position=Vector2(96,33);score.size=Vector2(size.x-159,54)
	var footer_height := 84.0 if landscape else 146.0
	footer.position=Vector2(0,size.y-footer_height);footer.size=Vector2(size.x,footer_height)
	var columns := 8 if landscape else 4
	var width := (size.x-12)/columns
	var height := 78.0 if landscape else 69.0
	for i in range(tabs.size()):
		var b := tabs[i]
		b.position=Vector2(6+(i%columns)*width,4+(i/columns)*(height+3))
		b.size=Vector2(width-4,height)
		b.get_child(0).position=Vector2((b.size.x-38)/2,1)
		b.get_child(0).size=Vector2(38,38)
		b.get_child(1).position=Vector2(2,39)
		b.get_child(1).size=Vector2(b.size.x-4,height-40)
		b.get_child(1).add_theme_font_size_override("font_size",12)
	world.position=Vector2(0,94)
	world.size=Vector2(size.x,maxf(140,size.y-94-footer_height))
	if is_instance_valid(chooser): arrange_chooser()
	queue_redraw()
func hero_name(id: String) -> String:
	if host.store.data.locale=="ru":
		var family: bool=preload("res://core/quest/cast.gd").FAMILY
		return Lang.data().heroes["family" if family else "neutral"][id]
	if not preload("res://core/quest/cast.gd").FAMILY and id!="squirrel": return preload("res://core/quest/hero.gd").NAMES[id]
	if id=="du": return host.t("self_hero")
	if id=="katze": return Lang.object_name("cat",host.store.data.locale)
	if id=="squirrel": return host.t("squirrel")
	return preload("res://core/quest/hero.gd").NAMES[id]
func open_task(index: int) -> void:
	if is_instance_valid(task_panel) or choosing: return
	last_station=index
	world.set_process(false)
	world.hero.animation = "think"
	task_panel = preload("res://games/quest/task.gd").new()
	add_child(task_panel)
	task_panel.setup(host,Progress.tasks(subject)[index])
	task_panel.closed.connect(close_task)
	task_panel.solved.connect(func(_id): update_score(true))
	task_panel.bonus_requested.connect(open_bonus)
func open_bonus(index: int) -> void:
	var parent: Dictionary=Progress.tasks(subject)[last_station]
	var bonuses: Array=parent.get("bonuses",[])
	if index<0 or index>=bonuses.size(): return
	host.narration.cancel()
	remove_child(task_panel);task_panel.queue_free()
	task_panel=preload("res://games/quest/task.gd").new()
	add_child(task_panel)
	task_panel.setup(host,bonuses[index],parent,index)
	task_panel.closed.connect(close_task)
	task_panel.solved.connect(func(_id): update_score(true))
	task_panel.bonus_requested.connect(open_bonus)
func close_task() -> void:
	if is_instance_valid(task_panel):
		if task_panel.complete:
			world.celebration = 1.2
			world.hero.react()
			world.advance_target = world.station_x(last_station)+120
		remove_child(task_panel)
		task_panel.queue_free()
		task_panel = null
		host.narration.cancel()
		world.set_process(true)
		world.hero.animation = "idle"
		world.queue_redraw()
func choose_hero() -> void:
	close_task()
	if is_instance_valid(chooser): return
	choosing = true
	world.set_process(false)
	chooser = Panel.new()
	chooser.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	var panel := StyleBoxFlat.new()
	panel.bg_color = Color("19384f")
	chooser.add_theme_stylebox_override("panel",panel)
	add_child(chooser)
	chooser_label = label(host.t("choose"),chooser)
	chooser_label.add_theme_color_override("font_color",Color("fff4dc"))
	hero_choices.clear()
	for id in preload("res://core/quest/hero.gd").IDS:
		var b := button("",func(): select_hero(id),chooser)
		b.tooltip_text = hero_name(id)
		var figure := preload("res://core/quest/hero.gd").new()
		figure.person = id
		figure.costume = host.store.data.looks[id]
		figure.animation = "idle"
		figure.reduced_motion = host.store.data.reduced_motion
		b.add_child(figure)
		var name_tag := label(b.tooltip_text,b)
		name_tag.add_theme_color_override("font_color",Color("fff4dc"))
		name_tag.add_theme_font_size_override("font_size",22)
		hero_choices.append(b)
	look_buttons.clear()
	for look in preload("res://core/quest/wardrobe.gd").LOOKS:
		var look_button:=button("",func(): select_look(look),chooser)
		look_button.add_theme_font_size_override("font_size",11)
		look_button.tooltip_text=host.t("look_"+look)
		var icon:=preload("res://core/quest/icon.gd").new()
		icon.object={"classic":"fabric","hero":"star","alien":"robot","astronaut":"helmet","scientist":"glass"}[look]
		look_button.add_child(icon)
		var caption:=label(host.t("look_"+look),look_button)
		caption.add_theme_font_size_override("font_size",10)
		caption.autowrap_mode=TextServer.AUTOWRAP_ARBITRARY
		look_buttons.append(look_button)
	start_button = button(host.t("start"),finish_hero,chooser)
	arrange_chooser()
	select_hero(host.store.data.hero)
	host.narration.play_clip("quest/choose",true)
func arrange_chooser() -> void:
	var landscape := size.x>size.y*1.3
	chooser_label.position = Vector2(12,12);chooser_label.size = Vector2(size.x-24,48)
	var count := hero_choices.size()
	var featured := count>=5 and count%2==1 and not landscape
	var columns := count if landscape else (3 if count>=7 else 2)
	var rows := 1 if landscape else (1+ceili((count-1)/float(columns)) if featured else ceili(count/float(columns)))
	var width := (size.x-28)/columns
	var height := (size.y-210)/rows
	for i in range(hero_choices.size()):
		var b := hero_choices[i]
		if featured:
			# The first hero leads the selection; the remaining choices stay equally reachable.
			b.position = Vector2(14,68) if i==0 else Vector2(14+((i-1)%columns)*width,68+(1+(i-1)/columns)*height)
			b.size = Vector2(size.x-36 if i==0 else width-8,height-6)
		else:
			b.position = Vector2(14+(i%columns)*width,68+(i/columns)*height)
			b.size = Vector2(width-8,height-6)
		var figure: Control = b.get_child(0)
		var h := minf(height-46,(b.size.x-8)/figure.aspect())
		figure.size = Vector2(h*figure.aspect(),h)
		figure.position = Vector2((b.size.x-figure.size.x)/2,maxf(0,(b.size.y-37-h)/2))
		var tag: Label = b.get_child(1)
		tag.position = Vector2(0,b.size.y-37);tag.size = Vector2(b.size.x,33)
		var px := 22
		while px>12 and Art.font().get_string_size(tag.text,HORIZONTAL_ALIGNMENT_LEFT,-1,px).x>b.size.x-8: px-=1
		tag.add_theme_font_size_override("font_size",px)
	for i in range(look_buttons.size()):
		look_buttons[i].position=Vector2(10+i*(size.x-20)/5,size.y-126)
		look_buttons[i].size=Vector2((size.x-20)/5-3,54)
		look_buttons[i].get_child(0).position=Vector2((look_buttons[i].size.x-26)/2,0)
		look_buttons[i].get_child(0).size=Vector2(26,26)
		look_buttons[i].get_child(1).position=Vector2(2,27)
		look_buttons[i].get_child(1).size=Vector2(look_buttons[i].size.x-4,26)
	start_button.position = Vector2(size.x*.14,size.y-65);start_button.size = Vector2(size.x*.72,52)
func refresh_looks() -> void:
	var looks: Array=preload("res://core/quest/wardrobe.gd").LOOKS
	for i in range(look_buttons.size()):
		var selected_look: bool=host.store.data.looks[host.store.data.hero]==looks[i]
		var style:=StyleBoxFlat.new()
		style.bg_color=Color("f8d382") if selected_look else Color("fff6df")
		style.set_corner_radius_all(18)
		look_buttons[i].add_theme_stylebox_override("normal",style)
func select_look(look: String) -> void:
	if look not in preload("res://core/quest/wardrobe.gd").LOOKS:return
	host.store.data.looks[host.store.data.hero]=look
	host.save()
	var index: int=preload("res://core/quest/hero.gd").IDS.find(host.store.data.hero)
	var figure: Control=hero_choices[index].get_child(0)
	figure.costume=look;figure.react()
	arrange_chooser();refresh_looks()
	host.narration.play_clip("quest/look_"+look,true)
func select_hero(id: String) -> void:
	host.store.data.hero = id
	host.save()
	refresh_looks()
	for i in range(hero_choices.size()):
		var chosen: bool = preload("res://core/quest/hero.gd").IDS[i]==id
		var style := StyleBoxFlat.new()
		style.bg_color = Color("31576b") if chosen else Color(1,1,1,0)
		style.set_corner_radius_all(34)
		style.border_color = Color("f7ca68") if chosen else Color(1,1,1,0)
		style.set_border_width_all(3)
		hero_choices[i].add_theme_stylebox_override("normal",style)
		hero_choices[i].get_child(0).selected = chosen
		if chosen: hero_choices[i].get_child(0).react()
		else: hero_choices[i].get_child(0).animation = "idle"
func finish_hero() -> void:
	host.store.data.quest.hero_chosen = true
	host.save()
	host.narration.cancel()
	remove_child(chooser);chooser.queue_free();chooser=null
	choosing = false
	world.hero.person = host.store.data.hero
	world.hero.costume = host.store.data.looks[host.store.data.hero]
	world.set_process(true)
	update_score()
	host.narration.play_clip("quest/world_"+world.scene_id() if world.scene_id() in ["tree","seabed","city","moon"] else "quest/walk",true)
func open_menu() -> void:
	if is_instance_valid(menu): return
	menu = Panel.new()
	menu.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	var panel := StyleBoxFlat.new()
	panel.bg_color = Color("e5f0e5")
	menu.add_theme_stylebox_override("panel",panel)
	add_child(menu)
	var box := VBoxContainer.new()
	box.set_anchors_and_offsets_preset(PRESET_CENTER)
	box.offset_left=-130;box.offset_right=130;box.offset_top=-159;box.offset_bottom=159
	box.add_theme_constant_override("separation",6)
	menu.add_child(box)
	for entry in [[host.t("return"),func(): remove_child(menu);menu.queue_free();menu=null],[host.t("subjects"),host.subjects],[host.t("scenery"),host.sceneries],[host.t("musicbox"),host.musicbox],[host.t("settings"),host.settings],[host.t("language"),host.languages]]:
		var b := button(entry[0],entry[1],box)
		b.custom_minimum_size = Vector2(240,48)
		b.add_theme_font_size_override("font_size",18)
func persist() -> void: host.save()
func _notification(what: int) -> void:
	if what==NOTIFICATION_APPLICATION_PAUSED and host!=null:
		world.cancel_gesture()
		persist()
func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO,size),Color("f5efd9"))
	if is_instance_valid(footer): draw_rect(Rect2(footer.position,footer.size),Color("fffdf4"))
	draw_line(Vector2(0,93),Vector2(size.x,93),Color("c6d5c3"),2)
