extends RefCounted
# Density mapping is explicit rather than fitting a 900 px desktop onto a phone.
static func logical_size(pixels: Vector2i, dpi: float) -> Vector2i:
	var density := maxf(dpi/160.0,1.0)
	if dpi<72 or dpi>1000: density=maxf(minf(pixels.x,pixels.y)/420.0,1.0)
	var logical := Vector2(pixels)/density
	# Protect unknown/unreliable vendor DPI from forcing unusably narrow layouts.
	var factor := maxf(1.0,360.0/maxf(logical.x,1.0))
	return Vector2i(ceil(logical.x*factor),ceil(logical.y*factor))

static func configure(window: Window, simulated_dpi := 0.0) -> void:
	if OS.get_name() == "Android" or simulated_dpi>0:
		window.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
		var target := logical_size(window.size,simulated_dpi if simulated_dpi>0 else DisplayServer.screen_get_dpi())
		if window.content_scale_size != target: window.content_scale_size = target
	else:
		# Desktop and headless regression viewports retain their actual dimensions.
		window.content_scale_size = Vector2i.ZERO
