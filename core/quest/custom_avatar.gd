extends RefCounted
# Device-local pixels only. Never retain the document URI or source metadata.
const PATH := "user://avatars/player.png"
const Codec=preload("res://core/quest/avatar_image.gd")
const MAX_BYTES := Codec.MAX_BYTES
const MAX_SIDE := Codec.MAX_SIDE
const MAX_PIXELS := Codec.MAX_PIXELS
const OUTPUT_SIDE := 512
const PADDING := 16
static var cached: ImageTexture
static var loaded := false

static func figure(image: Image) -> Image:
	var bounds:=image.get_used_rect()
	if bounds.size.x<=0 or bounds.size.y<=0:return null
	var result:=image.get_region(bounds)
	var scale:=minf(1.0,float(OUTPUT_SIDE-2*PADDING)/maxi(result.get_width(),result.get_height()))
	if scale<1:result.resize(maxi(1,roundi(result.get_width()*scale)),maxi(1,roundi(result.get_height()*scale)),Image.INTERPOLATE_LANCZOS)
	var padded:=Image.create(result.get_width()+2*PADDING,result.get_height()+2*PADDING,false,Image.FORMAT_RGBA8)
	padded.fill(Color.TRANSPARENT)
	padded.blit_rect(result,Rect2i(Vector2i.ZERO,result.get_size()),Vector2i(PADDING,PADDING))
	return padded

static func crop_rect(image: Image,center: Vector2,zoom: float) -> Rect2i:
	var side:=maxi(1,roundi(mini(image.get_width(),image.get_height())/clampf(zoom,1,4)))
	var at:=Vector2i(roundi(center.x*image.get_width()-side*.5),roundi(center.y*image.get_height()-side*.5))
	at.x=clampi(at.x,0,image.get_width()-side);at.y=clampi(at.y,0,image.get_height()-side)
	return Rect2i(at,Vector2i(side,side))

static func portrait(image: Image,center:=Vector2(.5,.5),zoom:=1.0) -> Image:
	var result:=image.get_region(crop_rect(image,center,zoom))
	var side:=mini(OUTPUT_SIDE,result.get_width())
	if result.get_width()>side:result.resize(side,side,Image.INTERPOLATE_LANCZOS)
	# Remove all RGBA data outside the circular frame, not just its alpha.
	var radius:=side*.5;var middle:=(side-1)*.5
	for y in range(side):
		var extent:=sqrt(maxf(0,radius*radius-pow(y-middle,2)))
		var left:=clampi(ceili(middle-extent),0,side)
		var right:=clampi(floori(middle+extent)+1,0,side)
		if left>0:result.fill_rect(Rect2i(0,y,left,1),Color.TRANSPARENT)
		if right<side:result.fill_rect(Rect2i(right,y,side-right,1),Color.TRANSPARENT)
	return result

static func prepare(data: PackedByteArray) -> Dictionary:
	var result:=Codec.decode(data)
	if result.error!="":return result
	var pixels: Image=result.image
	if pixels.get_used_rect().size==Vector2i.ZERO:return {"error":"avatar_empty"}
	var framed:=pixels.detect_alpha()==Image.ALPHA_NONE
	return {"error":"","image":portrait(pixels) if framed else figure(pixels),"pixels":pixels,"portrait":framed,"source_size":result.source_size}

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
		var file:=FileAccess.open(PATH,FileAccess.READ)
		if file==null:return null
		if file.get_length()>MAX_BYTES:file.close();return null
		var data:=file.get_buffer(MAX_BYTES+1);file.close()
		var result:=Codec.decode(data)
		if result.error=="" and result.format=="png" and result.image.get_used_rect().size!=Vector2i.ZERO:cached=ImageTexture.create_from_image(result.image)
	return cached

static func available() -> bool:
	return texture()!=null

static func store(image: Image) -> Error:
	if image==null or image.is_empty() or maxi(image.get_width(),image.get_height())>OUTPUT_SIDE or image.get_used_rect().size==Vector2i.ZERO: return ERR_INVALID_DATA
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
