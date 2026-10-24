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
var crop_controls: HBoxContainer
var figure_button: Button
var portrait_button: Button
var zoom_out: Button
var zoom_in: Button
var scroll: ScrollContainer

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
	scroll=ScrollContainer.new();scroll.horizontal_scroll_mode=ScrollContainer.SCROLL_MODE_DISABLED
	scroll.follow_focus=true;margin.add_child(scroll)
	column=VBoxContainer.new();column.size_flags_horizontal=SIZE_EXPAND_FILL
	column.add_theme_constant_override("separation",10);scroll.add_child(column)
	add_button(host.t("return"),close)
	add_label(host.t("avatar_title"),25)
	add_label(host.t("avatar_privacy"),17)
	if editable:choose_button=add_button("＋ "+host.t("avatar_pick"),open_picker)
	else:add_label(host.t("avatar_parent_hint"),20)
	add_button("? "+host.t("avatar_help"),func():help_text.visible=not help_text.visible)
	help_text=add_label(host.t("avatar_help_text"),19);help_text.visible=show_help and not editable
	message=add_label(host.t("avatar_preview_hint"),18)
	preview=preload("res://core/quest/avatar_preview.gd").new()
	preview.editable=editable
	preview.custom_minimum_size=Vector2(0,220);column.add_child(preview)
	preview.texture=Avatar.texture();preview.queue_redraw()
	resized.connect(update_preview_size)
	update_preview_size()
	host.narration.cancel()
	if not editable:
		message.visible=Avatar.available();preview.visible=Avatar.available()
		return
	var modes:=HBoxContainer.new();column.add_child(modes)
	figure_button=add_button(host.t("avatar_figure"),func():preview.set_portrait(false));column.remove_child(figure_button);modes.add_child(figure_button)
	portrait_button=add_button(host.t("avatar_portrait"),func():preview.set_portrait(true));column.remove_child(portrait_button);modes.add_child(portrait_button)
	for b in [figure_button,portrait_button]:b.size_flags_horizontal=SIZE_EXPAND_FILL;b.disabled=true
	add_label(host.t("avatar_crop_hint"),17)
	crop_controls=HBoxContainer.new();column.add_child(crop_controls)
	zoom_out=add_button("−",func():preview.set_zoom(preview.zoom/1.2));column.remove_child(zoom_out);crop_controls.add_child(zoom_out)
	var reset:=add_button(host.t("avatar_crop_reset"),func():preview.reset_crop());column.remove_child(reset);crop_controls.add_child(reset)
	zoom_in=add_button("＋",func():preview.set_zoom(preview.zoom*1.2));column.remove_child(zoom_in);crop_controls.add_child(zoom_in)
	zoom_out.accessibility_name=host.t("avatar_zoom_out");zoom_in.accessibility_name=host.t("avatar_zoom_in")
	for b in [zoom_out,reset,zoom_in]:b.size_flags_horizontal=SIZE_EXPAND_FILL
	crop_controls.hide()
	preview.changed.connect(sync_crop_controls)
	confirm_button=add_button(host.t("avatar_use"),confirm);confirm_button.disabled=true
	remove_button=add_button(host.t("avatar_remove"),erase);remove_button.visible=Avatar.available()
	picker=FileDialog.new();picker.use_native_dialog=true
	picker.access=FileDialog.ACCESS_FILESYSTEM
	picker.file_mode=FileDialog.FILE_MODE_OPEN_FILE
	picker.title=host.t("avatar_pick")
	picker.filters=PackedStringArray(["*.png;"+host.t("avatar_images")+";image/png","*.jpg,*.jpeg;"+host.t("avatar_images")+";image/jpeg","*.webp;"+host.t("avatar_images")+";image/webp"])
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
	preview.cancel_gesture()
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
		preview.source=null;preview.texture=null;preview.figure_texture=null;preview.refresh()
		figure_button.disabled=true;portrait_button.disabled=true;crop_controls.hide()
		return
	candidate=result.image
	help_text.hide()
	preview.set_source(result.pixels,result.portrait)
	message.text=host.t("avatar_preview_hint")
	confirm_button.disabled=false

func sync_crop_controls() -> void:
	if not editable or preview.source==null:return
	figure_button.disabled=preview.source.detect_alpha()==Image.ALPHA_NONE
	portrait_button.disabled=false
	figure_button.text=("✓ " if not preview.portrait else "")+host.t("avatar_figure")
	portrait_button.text=("✓ " if preview.portrait else "")+host.t("avatar_portrait")
	crop_controls.visible=preview.portrait
	zoom_out.disabled=preview.zoom<=1;zoom_in.disabled=preview.zoom>=4

func update_preview_size() -> void:
	if is_instance_valid(preview):preview.custom_minimum_size.y=clampf(size.y*.3,120,220)

func confirm() -> void:
	if not editable or candidate==null:return
	if preview.source!=null:candidate=preview.output()
	if candidate==null or candidate.get_used_rect().size==Vector2i.ZERO:
		message.text=host.t("avatar_empty");return
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
