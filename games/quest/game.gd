extends Control
const Progress = preload("res://games/quest/progress.gd")
const Art = preload("res://core/quest/art.gd")
const NAMES := {"math":"Mathe","german":"Deutsch","logic":"Logik"}
const COLORS := {"math":"b75a32","german":"3f7192","logic":"70568b"}
var host: Control
var world: Control
var task_panel: Control
var chooser: Control
var menu: Control
var subject := "math"
var title: Label
var score: Label
var hero_button: Button
var menu_button: Button
var tabs: Array[Button] = []
var footer: Control
var choosing := false
var hero_choices: Array[Button] = []
var start_button: Button
var chooser_label: Label
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
	hero_button = button("Figur",choose_hero)
	hero_button.tooltip_text = "Spielfigur wählen"
	menu_button = button("☰",open_menu)
	menu_button.text = ""
	var gear := preload("res://core/quest/icon.gd").new()
	gear.cell = Vector2i(0,1)
	gear.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	menu_button.add_child(gear)
	menu_button.tooltip_text = "Musik und Einstellungen"
	title = label("")
	score = label("")
	score.add_theme_font_size_override("font_size",16)
	footer = Control.new()
	add_child(footer)
	for id in Progress.SUBJECTS:
		var b := button("",func(): switch_subject(id),footer)
		b.tooltip_text = NAMES[id]
		var icon := preload("res://core/quest/icon.gd").new()
		icon.cell = Vector2i(Progress.SUBJECTS.find(id),0)
		b.add_child(icon)
		var caption := label(NAMES[id],b)
		caption.add_theme_font_size_override("font_size",18)
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
	title.text = NAMES[id]
	var done := Progress.tasks(subject).filter(func(t): return host.store.data.quest.solved.has(t.id)).size()
	if done>0 and done<8:
		var first: int = Progress.tasks(subject).find_custom(func(t): return not host.store.data.quest.solved.has(t.id))
		world.hero_x = world.station_x(first)-140
		world.target_x = world.hero_x
		world.camera_x = maxf(0,world.hero_x-size.x*.3)
	world.first_hint = done==0
	host.audio.set_world({"math":"math","german":"german","logic":"logic"}[id])
	update_score()
	arrange()
func update_score() -> void:
	var stars := Progress.stars(host.store.data.quest)
	score.text = "★ %d   ·   %d Punkte" % [stars,stars*10]
	hero_button.text = preload("res://core/quest/hero.gd").NAMES[host.store.data.hero]
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
	# A single fullscreen play surface. No nested scroll containers or tiny arrows.
	if OS.get_name()=="Android":
		var safe := DisplayServer.get_display_safe_area()
		var ratio := Vector2(get_window().content_scale_size)/Vector2(get_window().size)
		var origin := Vector2(get_window().position)
		offset_left = maxf(0,safe.position.x-origin.x)*ratio.x
		offset_top = maxf(0,safe.position.y-origin.y)*ratio.y
		offset_right = -maxf(0,get_window().size.x-safe.end.x+origin.x)*ratio.x
		offset_bottom = -maxf(0,get_window().size.y-safe.end.y+origin.y)*ratio.y
	hero_button.position = Vector2(10,10);hero_button.size = Vector2(83,48)
	menu_button.position = Vector2(size.x-60,10);menu_button.size = Vector2(50,48)
	title.position = Vector2(96,2);title.size = Vector2(size.x-159,33)
	score.position = Vector2(96,34);score.size = Vector2(size.x-159,28)
	footer.position = Vector2(0,size.y-102);footer.size = Vector2(size.x,102)
	for i in range(3):
		tabs[i].position = Vector2(8+i*(size.x-16)/3,5)
		tabs[i].size = Vector2((size.x-16)/3-5,90)
		tabs[i].get_child(0).position = Vector2((tabs[i].size.x-66)/2,-2)
		tabs[i].get_child(0).size = Vector2(66,66)
		tabs[i].get_child(1).position = Vector2(0,61)
		tabs[i].get_child(1).size = Vector2(tabs[i].size.x,25)
	world.position = Vector2(0,68)
	world.size = Vector2(size.x,maxf(170,size.y-170))
	if is_instance_valid(chooser): arrange_chooser()
	queue_redraw()
func open_task(index: int) -> void:
	if is_instance_valid(task_panel) or choosing: return
	last_station=index
	world.set_process(false)
	world.hero.animation = "think"
	task_panel = preload("res://games/quest/task.gd").new()
	add_child(task_panel)
	task_panel.setup(host,Progress.tasks(subject)[index])
	task_panel.closed.connect(close_task)
	task_panel.solved.connect(func(_id): update_score())
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
	chooser_label = label("Wer bist du heute?",chooser)
	chooser_label.add_theme_color_override("font_color",Color("fff4dc"))
	hero_choices.clear()
	for id in preload("res://core/quest/hero.gd").IDS:
		var b := button("",func(): select_hero(id),chooser)
		b.tooltip_text = preload("res://core/quest/hero.gd").NAMES[id]
		var figure := preload("res://core/quest/hero.gd").new()
		figure.person = id
		figure.animation = "idle"
		figure.reduced_motion = host.store.data.reduced_motion
		b.add_child(figure)
		var name_tag := label(b.tooltip_text,b)
		name_tag.add_theme_color_override("font_color",Color("fff4dc"))
		name_tag.add_theme_font_size_override("font_size",22)
		hero_choices.append(b)
	start_button = button("Los geht’s!  →",finish_hero,chooser)
	arrange_chooser()
	select_hero(host.store.data.hero)
	host.narration.play_clip("quest/choose",true)
func arrange_chooser() -> void:
	var landscape := size.x>size.y*1.3
	chooser_label.position = Vector2(12,12);chooser_label.size = Vector2(size.x-24,48)
	var columns := 4 if landscape else 2
	var rows := 1 if landscape else 2
	var width := (size.x-28)/columns
	var height := (size.y-144)/rows
	for i in range(hero_choices.size()):
		var b := hero_choices[i]
		b.position = Vector2(14+(i%columns)*width,68+(i/columns)*height)
		b.size = Vector2(width-8,height-8)
		var figure: Control = b.get_child(0)
		var h := height-40
		figure.size = Vector2(h*.67,h)
		figure.position = Vector2((b.size.x-figure.size.x)/2,0)
		var tag: Label = b.get_child(1)
		tag.position = Vector2(0,b.size.y-37);tag.size = Vector2(b.size.x,33)
	start_button.position = Vector2(size.x*.14,size.y-65);start_button.size = Vector2(size.x*.72,52)
func select_hero(id: String) -> void:
	host.store.data.hero = id
	host.save()
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
	world.set_process(true)
	update_score()
	host.narration.play_clip("quest/walk",true)
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
	box.offset_left=-130;box.offset_right=130;box.offset_top=-142;box.offset_bottom=142
	box.add_theme_constant_override("separation",12)
	menu.add_child(box)
	for entry in [["Zurück",func(): remove_child(menu);menu.queue_free();menu=null],["Figur wählen",func(): remove_child(menu);menu.queue_free();menu=null;choose_hero()],["Musikbox",host.musicbox],["Einstellungen",host.settings]]:
		var b := button(entry[0],entry[1],box)
		b.custom_minimum_size = Vector2(240,56)
func persist() -> void: host.save()
func _notification(what: int) -> void:
	if what==NOTIFICATION_APPLICATION_PAUSED and host!=null:
		world.cancel_gesture()
		persist()
func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO,size),Color("f5efd9"))
	draw_line(Vector2(0,67),Vector2(size.x,67),Color("c6d5c3"),2)
