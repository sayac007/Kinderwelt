extends Control
signal closed
signal solved(id: String)
const Art = preload("res://core/quest/art.gd")
const Progress = preload("res://games/quest/progress.gd")
var host: Control
var task: Dictionary
var picture: Control
var choices: Array[Button] = []
var heading: Label
var feedback: Label
var close_button: Button
var speaker: Button
var help_button: Button
var next_button: Button
var complete := false
var companion: Control
func setup(owner_host: Control,data: Dictionary) -> void:
	host = owner_host
	task = preload("res://core/quest/language.gd").task(data,host.store.data.locale)
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	mouse_filter = MOUSE_FILTER_STOP
	close_button = make_button("×",func(): host.narration.cancel();closed.emit())
	close_button.tooltip_text = host.t("walk_back")
	speaker = make_button("",repeat)
	preload("res://core/quest/transport_icons.gd").apply(speaker,"speaker",28)
	speaker.tooltip_text = host.t("repeat")
	heading = Label.new()
	heading.text = task.prompt if task.kind=="discovery" else host.t(task.kind)
	heading.max_lines_visible = 6 if task.kind=="discovery" else 2
	heading.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	heading.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	heading.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	heading.add_theme_font_size_override("font_size",roundi((18 if task.kind=="discovery" else 20)*host.store.data.text_scale))
	add_child(heading)
	picture = preload("res://games/quest/picture.gd").new()
	picture.task = task
	picture.host = host
	add_child(picture)
	companion = preload("res://core/quest/hero.gd").new()
	companion.person = host.store.data.hero
	companion.selected = true
	companion.reduced_motion = host.store.data.reduced_motion
	add_child(companion)
	companion.hide()
	for option in task.options:
		var b := make_button("",func(): answer(option))
		b.tooltip_text = preload("res://core/quest/language.gd").object_name(str(option),host.store.data.locale)
		var visual := preload("res://games/quest/choice.gd").new()
		visual.value = option
		visual.kind = task.kind
		if task.kind=="discovery": visual.caption = b.tooltip_text
		visual.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
		b.add_child(visual)
		choices.append(b)
	feedback = Label.new()
	feedback.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	feedback.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	feedback.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	feedback.add_theme_font_size_override("font_size",15)
	add_child(feedback)
	help_button = make_button(host.t("help"),help)
	next_button = make_button(host.t("next"),func(): host.narration.cancel();closed.emit())
	next_button.hide()
	resized.connect(arrange)
	arrange.call_deferred()
	host.narration.play_clip("quest/"+task.id,true)
func make_button(caption: String,action: Callable) -> Button:
	var b := Button.new()
	b.text = caption
	b.add_theme_font_size_override("font_size",22)
	b.pressed.connect(action)
	b.focus_mode = FOCUS_ALL
	add_child(b)
	return b
func arrange() -> void:
	if not is_instance_valid(picture): return
	var landscape := size.x>size.y*1.3
	close_button.position = Vector2(18,18);close_button.size = Vector2(52,52)
	speaker.position = Vector2(size.x-70,18);speaker.size = Vector2(52,52)
	heading.max_lines_visible = (3 if landscape else 6) if task.kind=="discovery" else (2 if landscape else 3)
	heading.position = Vector2(20,76) if not landscape else Vector2(78,14)
	heading.size = Vector2(size.x-40 if not landscape else size.x-156,0)
	var picture_top := heading.get_rect().end.y+12
	var picture_width := size.x-40 if not landscape else size.x*.55
	var picture_height := size.y-186-picture_top if not landscape else size.y-picture_top-21
	picture.position = Vector2(20,picture_top)
	picture.size = Vector2(picture_width,maxf(90,picture_height))
	var hero_height := minf(290,picture.size.y)
	companion.size = Vector2(hero_height*.67,hero_height)
	companion.position = picture.position+(picture.size-companion.size)/2
	var diameter := minf(88,(size.x-56)/3.0) if not landscape else 76.0
	var choice_y := size.y-174 if not landscape else 105.0
	var choice_center := size.x/2 if not landscape else size.x*.79
	for i in range(choices.size()):
		choices[i].size = Vector2.ONE*diameter
		choices[i].position = Vector2(choice_center+(i-(choices.size()-1)*.5)*(diameter+8)-diameter/2,choice_y)
		if task.kind=="compare":
			# Answer by touching the actual pile, not by decoding left/right arrows.
			choices[i].position = picture.position+Vector2(i*picture.size.x*.57,0)
			choices[i].size = Vector2(picture.size.x*.43,picture.size.y)
			choices[i].get_child(0).hide()
			for state in ["normal","hover","pressed","disabled"]: choices[i].add_theme_stylebox_override(state,StyleBoxEmpty.new())
	feedback.position = Vector2(20,size.y-102 if not landscape else 192)
	feedback.size = Vector2(size.x-40 if not landscape else size.x*.42,46)
	if landscape: feedback.position.x = size.x*.57
	help_button.position = Vector2(size.x/2-84,size.y-57)
	help_button.size = Vector2(168,48)
	next_button.position = help_button.position
	next_button.size = help_button.size
	queue_redraw()
func repeat() -> void: host.narration.play_clip("quest/"+task.id)
func help() -> void:
	picture.hint = true
	picture.queue_redraw()
	host.narration.play_clip("quest/"+task.id+"_hint")
	for i in range(choices.size()):
		if task.options[i]==task.answer:
			var frame := StyleBoxFlat.new()
			frame.bg_color = Color("e0f0df")
			frame.border_color = Color("237a79")
			frame.set_border_width_all(4)
			frame.set_corner_radius_all(38)
			choices[i].add_theme_stylebox_override("normal",frame)
	feedback.text = host.t("encourage")
func answer(value: Variant) -> void:
	if complete: return
	if Progress.correct(task,value):
		complete = true
		picture.hide()
		companion.show()
		companion.react()
		host.sound(true)
		var fresh := Progress.award(host.store.data.quest,task.id)
		host.save()
		feedback.text = host.t("reward" if fresh else "remembered")
		for i in range(choices.size()):
			choices[i].disabled=true
			if task.kind=="compare": choices[i].hide()
			elif Progress.same(task.options[i],task.answer):
				var frame:=StyleBoxFlat.new()
				frame.bg_color=Color("d9efdb");frame.border_color=Color("25775c")
				frame.set_border_width_all(3);frame.set_corner_radius_all(38)
				choices[i].add_theme_stylebox_override("disabled",frame)
			else: choices[i].modulate.a=.45
		help_button.hide()
		next_button.show()
		host.narration.play_clip("quest/success")
		solved.emit(task.id)
	else:
		feedback.text = host.t("again")
		host.narration.play_clip("quest/again")
	queue_redraw()
func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO,size),Color(0.09,.17,.23,.66))
	var panel := StyleBoxFlat.new()
	panel.bg_color = Color("fff9eb")
	panel.set_corner_radius_all(30)
	draw_style_box(panel,Rect2(Vector2(8,8),size-Vector2(16,16)))
