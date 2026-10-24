extends Control
signal imported
signal removed
signal closed
const Avatar=preload("res://core/quest/custom_avatar.gd")
var host: Control
var candidate: Image
var picker: FileDialog
var picking := false
var message: Label
var help_text: Label
var preview: Control
var confirm_button: Button
var choose_button: Button
var remove_button: Button
var column: VBoxContainer
var editable := false

func setup(owner_host: Control,show_help := false,allow_changes := false) -> void:
	host=owner_host
	editable=allow_changes
	set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	mouse_filter=MOUSE_FILTER_STOP
	var background:=Panel.new()
	background.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	var style:=StyleBoxFlat.new();style.bg_color=Color("19384f")
	background.add_theme_stylebox_override("panel",style);add_child(background)
	var margin:=MarginContainer.new()
	margin.set_anchors_and_offsets_preset(PRESET_FULL_RECT)
	for side in ["left","top","right","bottom"]:margin.add_theme_constant_override("margin_"+side,12)
	add_child(margin)
	var scroll:=ScrollContainer.new();scroll.horizontal_scroll_mode=ScrollContainer.SCROLL_MODE_DISABLED
	scroll.follow_focus=true;margin.add_child(scroll)
	column=VBoxContainer.new();column.size_flags_horizontal=SIZE_EXPAND_FILL
	column.add_theme_constant_override("separation",10);scroll.add_child(column)
	add_button(host.t("return"),close)
	add_label(host.t("avatar_title"),25)
	if editable:choose_button=add_button("＋ "+host.t("avatar_pick"),open_picker)
	else:add_label(host.t("avatar_parent_hint"),20)
	add_button("? "+host.t("avatar_help"),func():help_text.visible=not help_text.visible)
	help_text=add_label(host.t("avatar_help_text"),19);help_text.visible=show_help
	message=add_label(host.t("avatar_preview_hint"),18)
	preview=preload("res://core/quest/avatar_preview.gd").new()
	preview.custom_minimum_size=Vector2(0,220);column.add_child(preview)
	preview.texture=Avatar.texture();preview.queue_redraw()
	resized.connect(update_preview_size)
	update_preview_size()
	host.narration.cancel()
	if not editable:
		message.visible=Avatar.available();preview.visible=Avatar.available()
		return
	confirm_button=add_button(host.t("avatar_use"),confirm);confirm_button.disabled=true
	remove_button=add_button(host.t("avatar_remove"),erase);remove_button.visible=Avatar.available()
	picker=FileDialog.new();picker.use_native_dialog=true
	picker.access=FileDialog.ACCESS_FILESYSTEM
	picker.file_mode=FileDialog.FILE_MODE_OPEN_FILE
	picker.title=host.t("avatar_pick")
	picker.filters=PackedStringArray(["*.png;"+host.t("avatar_png")+";image/png"])
	picker.current_dir=OS.get_system_dir(OS.SYSTEM_DIR_DOWNLOADS)
	picker.file_selected.connect(load_path)
	picker.canceled.connect(func():picking=false;choose_button.disabled=false)
	add_child(picker)
	host.narration.cancel()

func add_button(caption: String,action: Callable) -> Button:
	var button:=Button.new();button.text=caption
	button.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	button.custom_minimum_size=Vector2(0,52)
	button.add_theme_font_size_override("font_size",20)
	button.accessibility_name=caption
	button.pressed.connect(action);column.add_child(button)
	return button

func add_label(caption: String,font_size: int) -> Label:
	var label:=Label.new();label.text=caption
	label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART
	label.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER
	label.add_theme_color_override("font_color",Color("fff4dc"))
	label.add_theme_font_size_override("font_size",font_size)
	column.add_child(label)
	return label

func open_picker() -> void:
	if not editable or picking:return
	if OS.get_name()=="Android" and not DisplayServer.has_feature(DisplayServer.FEATURE_NATIVE_DIALOG_FILE):
		message.text=host.t("avatar_native_unavailable")
		return
	picking=true;choose_button.disabled=true
	picker.popup_centered_ratio(.9)

func load_path(path: String) -> void:
	if not editable:return
	picking=false;choose_button.disabled=true;confirm_button.disabled=true
	candidate=null
	message.text=host.t("avatar_loading")
	await get_tree().process_frame
	if not is_inside_tree():return
	var result:=Avatar.read_image(path)
	choose_button.disabled=false
	if result.error!="":
		message.text=host.t(result.error)
		help_text.show()
		preview.texture=null;preview.queue_redraw()
		return
	candidate=result.image
	help_text.hide()
	preview.texture=ImageTexture.create_from_image(candidate);preview.queue_redraw()
	message.text=host.t("avatar_preview_hint")
	confirm_button.disabled=false

func update_preview_size() -> void:
	if is_instance_valid(preview):preview.custom_minimum_size.y=clampf(size.y*.3,120,220)

func confirm() -> void:
	if not editable or candidate==null:return
	if Avatar.store(candidate)!=OK:
		message.text=host.t("avatar_save_failed")
		return
	imported.emit()

func erase() -> void:
	if not editable:return
	if Avatar.erase()!=OK:
		message.text=host.t("avatar_save_failed")
		return
	removed.emit()

func close() -> void:
	closed.emit()
	queue_free()

func handle_back() -> void:
	if picking:
		picking=false;choose_button.disabled=false
		picker.hide()
	else:close()
