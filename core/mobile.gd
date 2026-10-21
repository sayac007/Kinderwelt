extends RefCounted
# Preserve aspect ratio and the same minimum short side in BOTH orientations.
static func logical_size(pixels: Vector2i,dpi: float) -> Vector2i:
	if pixels.x<=0 or pixels.y<=0: return Vector2i(360,640)
	var density := maxf(dpi/160.0,1.0)
	if dpi<72 or dpi>1000: density=maxf(minf(pixels.x,pixels.y)/420.0,1.0)
	var logical := Vector2(pixels)/density
	var factor := maxf(1.0,360.0/minf(logical.x,logical.y))
	return Vector2i(round(logical.x*factor),round(logical.y*factor))
static func safe_insets(pixels: Vector2i,logical: Vector2i,safe: Rect2i,origin := Vector2i.ZERO) -> Vector4:
	if pixels.x<=0 or pixels.y<=0 or logical.x<=0 or logical.y<=0: return Vector4.ZERO
	var local := Rect2i(safe.position-origin,safe.size)
	# Android can briefly return the previous orientation's rectangle during rotation.
	if not Rect2i(Vector2i.ZERO,pixels).encloses(local) or local.size.x<=0 or local.size.y<=0: return Vector4.ZERO
	var ratio := Vector2(logical)/Vector2(pixels)
	return Vector4(local.position.x*ratio.x,local.position.y*ratio.y,(pixels.x-local.end.x)*ratio.x,(pixels.y-local.end.y)*ratio.y)
static func configure(window: Window,simulated_dpi := 0.0) -> void:
	if window.size.x<100 or window.size.y<100: return
	if OS.get_name()=="Android" or simulated_dpi>0:
		window.content_scale_mode=Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
		window.content_scale_aspect=Window.CONTENT_SCALE_ASPECT_EXPAND
		var target := logical_size(window.size,simulated_dpi if simulated_dpi>0 else DisplayServer.screen_get_dpi())
		if window.content_scale_size!=target: window.content_scale_size=target
	else: window.content_scale_size=Vector2i.ZERO
