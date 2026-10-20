extends VBoxContainer
const Tracks = preload("res://core/modern/tracks.gd")
var host: Control
var covers := {}
var current: Label
var favorite: Button
var shuffle: Button
func setup(parent: Control) -> void:
	host = parent
	host.button("⌂ Karte",host.hub,self)
	current = Label.new()
	current.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	current.add_theme_font_size_override("font_size",22)
	add_child(current)
	var controls := HBoxContainer.new()
	add_child(controls)
	transport(controls,"previous","Voriger Titel",func(): step(-1))
	transport(controls,"play","Titel anhören",func(): select(selected()))
	transport(controls,"next","Nächster Titel",func(): step(1))
	var options := HBoxContainer.new()
	add_child(options)
	shuffle = host.button("",toggle_shuffle,options)
	favorite = host.button("",toggle_favorite,options)
	var grid := GridContainer.new()
	grid.columns = 2
	add_child(grid)
	for id in Tracks.ITEMS:
		var b: Button = host.button("",func(): select(id),grid)
		b.custom_minimum_size = Vector2(140,176)
		b.tooltip_text = Tracks.ITEMS[id].title
		var art := preload("res://core/modern/cover.gd").new()
		art.track = id
		art.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		art.offset_bottom = -54
		b.add_child(art)
		var title := Label.new()
		title.text = Tracks.ITEMS[id].title
		title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		title.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		title.mouse_filter = Control.MOUSE_FILTER_IGNORE
		title.add_theme_font_size_override("font_size",18)
		title.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_WIDE)
		title.offset_top = -56
		b.add_child(title)
		covers[id] = b
	host.audio.music.set_world(selected())
	refresh()
func selected() -> String:
	var id: String = host.store.data.music_track
	return id if Tracks.ITEMS.has(id) else "adventure_workshop"
func select(id: String) -> void:
	if not Tracks.ITEMS.has(id): return
	host.store.data.music_track = id
	host.audio.music.set_world(id)
	host.save()
	refresh()
func step(direction: int) -> void:
	var ids: Array = Tracks.ITEMS.keys()
	var index := ids.find(selected())
	if host.store.data.music_shuffle and direction>0:
		var options := ids.duplicate()
		options.erase(selected())
		select(options.pick_random())
	else: select(ids[posmod(index+direction,ids.size())])
func toggle_shuffle() -> void:
	host.store.data.music_shuffle = not host.store.data.music_shuffle
	host.save()
	refresh()
func toggle_favorite() -> void:
	host.store.data.music_locked = not host.store.data.music_locked
	host.save()
	refresh()
func refresh() -> void:
	current.text = "♫ "+Tracks.ITEMS[selected()].title
	favorite.text = "♥ Bleibt" if host.store.data.music_locked else "♡ Merken"
	shuffle.text = "✓ Zufall" if host.store.data.music_shuffle else "⤨ Zufall"
	for id in covers:
		covers[id].add_theme_stylebox_override("normal",preload("res://core/design.gd").style(Color("e1ead3") if selected()==id else Color("fffdf6")))
		covers[id].get_child(1).text = ("✓ " if selected()==id else "")+Tracks.ITEMS[id].title

func transport(parent: Node,icon: String,title: String,action: Callable) -> void:
	var b: Button = host.button("",action,parent)
	b.tooltip_text = title
	preload("res://core/modern/icons.gd").apply(b,icon,32)
	b.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
