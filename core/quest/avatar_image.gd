extends RefCounted
# Bounded headers before decode; only oriented pixel data survives this module.
const MAX_BYTES := 20 * 1024 * 1024
const MAX_SIDE := 4096
const MAX_PIXELS := 16 * 1024 * 1024
const WORK_SIDE := 1024

static func u16(b: PackedByteArray,p: int,little := false) -> int:
	return int(b[p])|(int(b[p+1])<<8) if little else (int(b[p])<<8)|int(b[p+1])
static func u32(b: PackedByteArray,p: int,little := false) -> int:
	return u16(b,p,true)|(u16(b,p+2,true)<<16) if little else (u16(b,p)<<16)|u16(b,p+2)
static func ascii(b: PackedByteArray,p: int,n: int) -> String:
	return b.slice(p,p+n).get_string_from_ascii()

static func orientation(bytes: PackedByteArray) -> int:
	var b:=bytes.slice(6) if bytes.size()>=6 and bytes.slice(0,6)==PackedByteArray([69,120,105,102,0,0]) else bytes
	if b.size()<8:return 1
	var little:=ascii(b,0,2)=="II"
	if not little and ascii(b,0,2)!="MM":return 1
	if u16(b,2,little)!=42:return 1
	var at:=u32(b,4,little)
	if at<8 or at+2>b.size():return 1
	var count:=u16(b,at,little)
	if count>256 or at+2+count*12>b.size():return 1
	for i in range(count):
		var p:=at+2+i*12
		if u16(b,p,little)==274 and u16(b,p+2,little)==3 and u32(b,p+4,little)==1:
			var value:=u16(b,p+8,little)
			return value if value>=1 and value<=8 else 1
	return 1

static func png(b: PackedByteArray) -> Dictionary:
	if b.size()<33 or u32(b,8)!=13 or ascii(b,12,4)!="IHDR":return {}
	var result: Dictionary={"format":"png","width":u32(b,16),"height":u32(b,20),"orientation":1}
	var p:=8
	var pixels:=false
	while p+12<=b.size():
		var n:=u32(b,p)
		if n>b.size()-p-12:return {}
		var kind:=ascii(b,p+4,4)
		if kind=="acTL":return {} # Animated inputs are not character animations.
		if kind=="eXIf":result.orientation=orientation(b.slice(p+8,p+8+n))
		if kind=="IDAT":pixels=true
		p+=n+12
		if kind=="IEND":return result if n==0 and pixels and p==b.size() else {}
	return {}

static func jpeg(b: PackedByteArray) -> Dictionary:
	if b.size()<4 or b.slice(b.size()-2)!=PackedByteArray([255,217]):return {}
	var result: Dictionary={"format":"jpeg","width":0,"height":0,"orientation":1}
	var p:=2
	while p+1<b.size():
		if b[p]!=255:return {}
		while p<b.size() and b[p]==255:p+=1
		if p>=b.size():return {}
		var marker:=int(b[p]);p+=1
		if marker==217:return {}
		if marker==1 or (marker>=208 and marker<=215):continue
		if p+2>b.size():return {}
		var n:=u16(b,p)
		if n<2 or n>b.size()-p:return {}
		if marker in [192,193,194]:
			if n<8 or result.width!=0:return {}
			result.width=u16(b,p+5);result.height=u16(b,p+3)
		if marker==225 and n>=8 and b.slice(p+2,p+8)==PackedByteArray([69,120,105,102,0,0]):
			result.orientation=orientation(b.slice(p+2,p+n))
		if marker==218:return result if result.width>0 and result.height>0 else {}
		p+=n
	return {}

static func webp(b: PackedByteArray) -> Dictionary:
	if b.size()<20 or u32(b,4,true)+8!=b.size():return {}
	var result: Dictionary={"format":"webp","width":0,"height":0,"orientation":1}
	var canvas:=Vector2i.ZERO
	var p:=12
	while p+8<=b.size():
		var kind:=ascii(b,p,4);var n:=u32(b,p+4,true);var at:=p+8
		if n>b.size()-at:return {}
		if kind in ["ANIM","ANMF"]:return {}
		if kind=="VP8X":
			if n!=10 or b[at]&2:return {}
			canvas=Vector2i(1+int(b[at+4])+(int(b[at+5])<<8)+(int(b[at+6])<<16),1+int(b[at+7])+(int(b[at+8])<<8)+(int(b[at+9])<<16))
		if kind in ["VP8 ","VP8L"]:
			if result.width!=0:return {}
			if kind=="VP8 ":
				if n<10 or b.slice(at+3,at+6)!=PackedByteArray([157,1,42]):return {}
				result.width=u16(b,at+6,true)&16383;result.height=u16(b,at+8,true)&16383
			else:
				if n<5 or b[at]!=47:return {}
				var bits:=u32(b,at+1,true)
				if bits>>29!=0:return {}
				result.width=1+(bits&16383);result.height=1+((bits>>14)&16383)
		if kind=="EXIF":result.orientation=orientation(b.slice(at,at+n))
		p=at+n+(n%2)
	if p!=b.size() or result.width<=0 or result.height<=0:return {}
	if canvas!=Vector2i.ZERO and canvas!=Vector2i(result.width,result.height):return {}
	return result

static func decode(b: PackedByteArray) -> Dictionary:
	if b.size()>MAX_BYTES:return {"error":"avatar_too_large"}
	var header: Dictionary={}
	if b.size()>=8 and b.slice(0,8)==PackedByteArray([137,80,78,71,13,10,26,10]):header=png(b)
	elif b.size()>=3 and b[0]==255 and b[1]==216 and b[2]==255:header=jpeg(b)
	elif b.size()>=12 and ascii(b,0,4)=="RIFF" and ascii(b,8,4)=="WEBP":header=webp(b)
	else:return {"error":"avatar_format"}
	if header.is_empty() or header.width<=0 or header.height<=0:return {"error":"avatar_invalid"}
	if header.width>MAX_SIDE or header.height>MAX_SIDE or header.width*header.height>MAX_PIXELS:return {"error":"avatar_too_large"}
	var image:=Image.new();var error: Error=ERR_INVALID_DATA
	match header.format:
		"png":error=image.load_png_from_buffer(b)
		"jpeg":error=image.load_jpg_from_buffer(b)
		"webp":error=image.load_webp_from_buffer(b)
	if error!=OK or image.get_width()!=header.width or image.get_height()!=header.height:return {"error":"avatar_invalid"}
	image.convert(Image.FORMAT_RGBA8)
	match int(header.orientation):
		2:image.flip_x()
		3:image.flip_x();image.flip_y()
		4:image.flip_y()
		5:image.rotate_90(CLOCKWISE);image.flip_x()
		6:image.rotate_90(CLOCKWISE)
		7:image.rotate_90(CLOCKWISE);image.flip_y()
		8:image.rotate_90(COUNTERCLOCKWISE)
	var scale:=minf(1.0,float(WORK_SIDE)/maxi(image.get_width(),image.get_height()))
	if scale<1:image.resize(maxi(1,roundi(image.get_width()*scale)),maxi(1,roundi(image.get_height()*scale)),Image.INTERPOLATE_LANCZOS)
	return {"error":"","image":image,"format":header.format,"source_size":Vector2i(header.width,header.height)}
