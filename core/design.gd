extends RefCounted
# Logical UI units. Android maps these to density-independent units in mobile.gd.
const BACKGROUND := Color("fbf8f0")
const SURFACE := Color("ffffff")
const INK := Color("26372f")
const SECONDARY := Color("46584e")
const BORDER := Color("687c70")
const FOCUS := Color("285c46")
const ACCENTS := {"logic":"3c654e", "math":"814421", "language":"675080", "autonomy":"285d78", "social":"8b4255"}
const FONT := 23
const CAPTION := 18
const TOUCH := Vector2(96,80)

static func font_size(base: int,scale := 1.0) -> int:
	return roundi(base*clampf(scale,1.0,1.15))

static func style(fill: Color, border := BORDER) -> StyleBoxFlat:
	var box := StyleBoxFlat.new()
	box.bg_color = fill
	box.border_color = border
	box.set_border_width_all(2)
	box.set_corner_radius_all(18)
	box.content_margin_left = 10
	box.content_margin_right = 10
	box.content_margin_top = 10
	box.content_margin_bottom = 10
	return box

static func make_theme() -> Theme:
	var theme := Theme.new()
	theme.default_font_size = FONT
	for kind in ["Label","Button","CheckButton"]:
		theme.set_color("font_color",kind,INK)
		theme.set_color("font_hover_color",kind,INK)
		theme.set_color("font_pressed_color",kind,INK)
		theme.set_color("font_focus_color",kind,INK)
		theme.set_color("font_disabled_color",kind,SECONDARY)
	for state in ["normal","hover","pressed","disabled"]:
		var color := SURFACE if state == "normal" else Color("e4eee4")
		if state == "pressed": color = Color("c8dfce")
		theme.set_stylebox(state,"Button",style(color))
	var focus := style(Color(0,0,0,0),FOCUS)
	focus.set_border_width_all(4)
	theme.set_stylebox("focus","Button",focus)
	theme.set_constant("separation","VBoxContainer",16)
	theme.set_constant("h_separation","GridContainer",8)
	theme.set_constant("v_separation","GridContainer",12)
	return theme

static func luminance(c: Color) -> float:
	var rgb := []
	for value in [c.r,c.g,c.b]: rgb.append(value/12.92 if value<=0.04045 else pow((value+0.055)/1.055,2.4))
	return 0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2]

static func contrast(a: Color,b: Color) -> float:
	return (maxf(luminance(a),luminance(b))+0.05)/(minf(luminance(a),luminance(b))+0.05)
