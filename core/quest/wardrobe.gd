extends RefCounted
const LOOKS := ["classic","hero","alien","astronaut","scientist"]
const ATLASES = {
"wanja":preload("res://assets/quest/looks-wanja.png"),
"mischa":preload("res://assets/quest/looks-mischa.png"),
"du":preload("res://assets/quest/looks-du.png"),
"mama":preload("res://assets/quest/looks-mama.png"),
"katze":preload("res://assets/quest/looks-katze.png"),
"george":preload("res://assets/quest/looks-george.png"),
"squirrel":preload("res://assets/quest/looks-squirrel.png")}
static var catalog := {}
static var textures := {}
static var masks := {}
static func frame(person: String,look: String) -> AtlasTexture:
	if look not in LOOKS or look=="classic" or not ATLASES.has(person): return null
	if catalog.is_empty(): catalog=JSON.parse_string(FileAccess.get_file_as_string("res://assets/quest/looks.json"))
	var key := person+"/"+look
	if textures.has(key): return textures[key]
	var rect: Array=catalog.heroes[person].frames[look]
	var result:=AtlasTexture.new()
	result.atlas=ATLASES[person]
	result.region=Rect2(rect[0],rect[1],rect[2],rect[3])
	result.filter_clip=true
	textures[key]=result
	return result

static func mask(person: String) -> ImageTexture:
	if masks.has(person):return masks[person]
	var data: Dictionary=catalog.heroes[person]
	var image:=Image.create(data.pixels[0],data.pixels[1],false,Image.FORMAT_R8)
	for run in data.mask_runs:
		image.fill_rect(Rect2i(run[1],run[0],run[2],1),Color(float(run[3])/255.0,0,0))
	var texture:=ImageTexture.create_from_image(image)
	masks[person]=texture
	return texture
