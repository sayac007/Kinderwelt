extends RefCounted
const FOCUS:=Color("17597d")
static func style(fill: Color,border:=FOCUS) -> StyleBoxFlat:
	var b:=StyleBoxFlat.new();b.bg_color=fill;b.border_color=border
	b.set_corner_radius_all(28);b.set_border_width_all(2)
	return b
static func make_theme() -> Theme:
	var t:=Theme.new()
	t.default_font=preload("res://core/quest/art.gd").font()
	t.default_font_size=22
	for type in ["Button","Label"]:
		for name in ["font_color","font_hover_color","font_pressed_color","font_focus_color","font_disabled_color"]: t.set_color(name,type,Color("293b4c"))
	for state in ["normal","hover","pressed","disabled","focus"]:
		var b:=StyleBoxFlat.new();b.set_corner_radius_all(28)
		b.bg_color=Color("fff8e9") if state!="pressed" else Color("fae3b4")
		b.border_color=Color("617581") if state!="focus" else Color("17597d")
		b.set_border_width_all(2 if state!="focus" else 4)
		b.content_margin_left=10;b.content_margin_right=10
		b.content_margin_top=8;b.content_margin_bottom=8
		t.set_stylebox(state,"Button",b)
	return t
