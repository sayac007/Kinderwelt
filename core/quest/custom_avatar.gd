extends RefCounted
# Device-local pixels only. Never retain the document URI or source metadata.
const PATH := "user://avatars/player.png"
const MAX_BYTES := 10 * 1024 * 1024
const MAX_SIDE := 4096
const MAX_PIXELS := 16 * 1024 * 1024
const OUTPUT_SIDE := 1024
const PADDING := 16
static var cached: ImageTexture
static var loaded := false

static func big_endian(data: PackedByteArray, at: int) -> int:
	return (int(data[at]) << 24) | (int(data[at+1]) << 16) | (int(data[at+2]) << 8) | int(data[at+3])

static func prepare(data: PackedByteArray) -> Dictionary:
	if data.size() > MAX_BYTES: return {"error":"avatar_too_large"}
	if data.size()<33 or data.slice(0,8)!=PackedByteArray([137,80,78,71,13,10,26,10]):
		return {"error":"avatar_png_only"}
	if big_endian(data,8)!=13 or data.slice(12,16).get_string_from_ascii()!="IHDR":
		return {"error":"avatar_invalid"}
	var width := big_endian(data,16)
	var height := big_endian(data,20)
	if width<=0 or height<=0: return {"error":"avatar_invalid"}
	if width>MAX_SIDE or height>MAX_SIDE or width*height>MAX_PIXELS:
		return {"error":"avatar_too_large"}
	# Bound every PNG chunk before handing the stream to the decoder.
	var position := 8
	var has_pixels := false
	var ended := false
	while position+12<=data.size():
		var count := big_endian(data,position)
		if count>data.size()-position-12: return {"error":"avatar_invalid"}
		var kind := data.slice(position+4,position+8).get_string_from_ascii()
		if kind=="IDAT": has_pixels=true
		position+=count+12
		if kind=="IEND":
			ended=count==0
			break
	if not ended or not has_pixels: return {"error":"avatar_invalid"}
	var image := Image.new()
	if image.load_png_from_buffer(data)!=OK: return {"error":"avatar_invalid"}
	image.convert(Image.FORMAT_RGBA8)
	var bounds := image.get_used_rect()
	if bounds.size.x<=0 or bounds.size.y<=0: return {"error":"avatar_empty"}
	if image.detect_alpha()==Image.ALPHA_NONE: return {"error":"avatar_opaque"}
	image=image.get_region(bounds)
	var scale := minf(1.0,float(OUTPUT_SIDE-2*PADDING)/maxi(image.get_width(),image.get_height()))
	if scale<1.0:
		image.resize(maxi(1,roundi(image.get_width()*scale)),maxi(1,roundi(image.get_height()*scale)),Image.INTERPOLATE_LANCZOS)
	var result := Image.create(image.get_width()+2*PADDING,image.get_height()+2*PADDING,false,Image.FORMAT_RGBA8)
	result.fill(Color.TRANSPARENT)
	result.blit_rect(image,Rect2i(Vector2i.ZERO,image.get_size()),Vector2i(PADDING,PADDING))
	return {"error":"","image":result,"source_size":Vector2i(width,height)}

static func read_image(path: String) -> Dictionary:
	var file := FileAccess.open(path,FileAccess.READ)
	if file==null: return {"error":"avatar_read_failed"}
	if file.get_length()>MAX_BYTES:
		file.close()
		return {"error":"avatar_too_large"}
	# Also bound reads for document providers whose declared length is unknown.
	var bytes := file.get_buffer(MAX_BYTES+1)
	file.close()
	return prepare(bytes)

static func texture() -> ImageTexture:
	if loaded: return cached
	loaded=true
	if FileAccess.file_exists(PATH):
		var result := read_image(PATH)
		if result.error=="": cached=ImageTexture.create_from_image(result.image)
	return cached

static func available() -> bool:
	return texture()!=null

static func store(image: Image) -> Error:
	if image==null or image.is_empty(): return ERR_INVALID_DATA
	if DirAccess.make_dir_recursive_absolute("user://avatars")!=OK: return ERR_CANT_CREATE
	var error := image.save_png(PATH+".tmp")
	if error!=OK: return error
	error=DirAccess.rename_absolute(PATH+".tmp",PATH)
	if error!=OK:
		DirAccess.remove_absolute(PATH+".tmp")
		return error
	cached=ImageTexture.create_from_image(image)
	loaded=true
	return OK

static func erase() -> Error:
	if FileAccess.file_exists(PATH+".tmp"):
		var pending_error:=DirAccess.remove_absolute(PATH+".tmp")
		if pending_error!=OK:return pending_error
	if FileAccess.file_exists(PATH):
		var error := DirAccess.remove_absolute(PATH)
		if error!=OK: return error
	invalidate()
	return OK

static func invalidate() -> void:
	cached=null
	loaded=false
