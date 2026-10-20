extends VBoxContainer
const Tracks = preload("res://core/quest/tracks.gd")
var host: Control
var covers := {}
var current: Label
var favorite: Button
var shuffle: Button
func setup(parent: Control) -> void:
	host = parent
	host.button(host.t("back"),host.hub,self)
	current = Label.new()
	current.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	current.add_theme_font_size_override("font_size",22)
	add_child(current)
	var note := Label.new()
	note.text = host.t("playlist_note")
	note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	note.add_theme_font_size_override("font_size",18)
	add_child(note)
	var controls := HBoxContainer.new()
	add_child(controls)
	transport(controls,"previous",host.t("previous_track"),func(): step(-1))
	transport(controls,"play",host.t("play_track"),func(): select(selected()))
	transport(controls,"next",host.t("next_track"),func(): step(1))
	var options := HBoxContainer.new()
	add_child(options)
	shuffle = host.button("",toggle_shuffle,options)
	favorite = host.button("",toggle_favorite,options)
	var grid := GridContainer.new()
	grid.columns = 2
	add_child(grid)
	for id in Tracks.ITEMS:
		var b: Button = host.button("",func(): select(id),grid)
		b.custom_minimum_size = Vector2(140,208)
		b.tooltip_text = Tracks.ITEMS[id].composer+" · "+Tracks.ITEMS[id].title+" · "+Tracks.ITEMS[id].detail
		var art := preload("res://core/quest/cover.gd").new()
		art.track = id
		art.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		art.offset_bottom = -88
		b.add_child(art)
		var title := Label.new()
		title.text = Tracks.ITEMS[id].title
		title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		title.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		title.mouse_filter = Control.MOUSE_FILTER_IGNORE
		title.add_theme_font_size_override("font_size",17)
		title.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
		title.offset_top = -88
		b.add_child(title)
		covers[id] = b
	host.audio.music.set_world(selected())
	host.audio.music.track_changed.connect(on_track_changed)
	refresh()
func selected() -> String:
	var id: String = host.store.data.music_track
	return id if Tracks.ITEMS.has(id) else Tracks.DEFAULT
func select(id: String) -> void:
	if not Tracks.ITEMS.has(id): return
	host.store.data.music_track = id
	host.audio.music.set_world(id,true)
	host.save()
	refresh()
func step(direction: int) -> void:
	select(Tracks.next(selected(),direction,host.store.data.music_shuffle))
func toggle_shuffle() -> void:
	host.store.data.music_shuffle = not host.store.data.music_shuffle
	host.save()
	refresh()
func toggle_favorite() -> void:
	host.store.data.music_locked = not host.store.data.music_locked
	host.save()
	refresh()
func refresh() -> void:
	current.text = "♫ "+Tracks.ITEMS[selected()].composer+" · "+Tracks.ITEMS[selected()].title
	favorite.text = host.t("favorite_on" if host.store.data.music_locked else "favorite_off")
	shuffle.text = ("✓ " if host.store.data.music_shuffle else "⤨ ")+host.t("shuffle")
	for id in covers:
		covers[id].add_theme_stylebox_override("normal",preload("res://core/quest/theme.gd").style(Color("e1ead3") if selected()==id else Color("fffdf6")))
		covers[id].get_child(1).text = ("✓ " if selected()==id else "")+Tracks.ITEMS[id].composer+"\n"+Tracks.ITEMS[id].title+"\n"+Tracks.ITEMS[id].detail

func on_track_changed(_id: String) -> void: refresh()

func transport(parent: Node,icon: String,title: String,action: Callable) -> void:
	var b: Button = host.button("",action,parent)
	b.tooltip_text = title
	preload("res://core/quest/transport_icons.gd").apply(b,icon,32)
	b.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
