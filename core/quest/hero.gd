extends Control
# Each sprite is split at the hips: legs swing around their hip independently.
# The upper body, head and backpack remain readable during walking/celebration.
const NAMES := {"wanja":"Wanja","mischa":"Mischa","du":"Du","mama":"Mama","katze":"Katze"}
const IDS := ["wanja","mischa","du","mama","katze"]
const SPRITES = {"wanja":preload("res://assets/quest/wanja.png"),"mischa":preload("res://assets/quest/mischa.png"),"du":preload("res://assets/quest/du.png"),"mama":preload("res://assets/quest/mama.png"),"katze":preload("res://assets/quest/katze.png")}
var person := "wanja"
var animation := "idle"
var clock := 0.0
var reduced_motion := false
var facing := 1.0
var selected := false
var reaction := 0.0
var pet: MeshInstance2D
var pet_size := Vector2.ZERO
func react() -> void:
	reaction = 1.2
	animation = "success"
func _ready() -> void:
	mouse_filter = MOUSE_FILTER_IGNORE
	pet = MeshInstance2D.new()
	pet.texture = SPRITES.katze
	var shader_material := ShaderMaterial.new()
	shader_material.shader = preload("res://core/quest/pet.gdshader")
	pet.material = shader_material
	pet.hide()
	add_child(pet)
func _process(delta: float) -> void:
	if not reduced_motion: clock += delta
	if reaction>0:
		reaction = maxf(0,reaction-delta)
		if reaction==0: animation="idle"
	queue_redraw()
func _draw() -> void:
	var texture: Texture2D = SPRITES.get(person,SPRITES.wanja)
	var col := maxi(IDS.find(person),0)
	var w := float(texture.get_width())
	var h := float(texture.get_height())
	var scale_size := Vector2(size.x,size.y)
	var hue: float = [.02,.51,.61,.35,.77][col]
	if reaction>0 and not reduced_motion: hue+=reaction*.16
	var glow := Color.from_hsv(fposmod(hue+(.08*sin(clock*1.7) if selected and not reduced_motion else 0),1),.68,1)
	var intensity := .8 if selected else .24
	if reaction>0: intensity=1.0
	draw_set_transform(Vector2(size.x*.5,size.y*.51),0,Vector2(.62,1.2))
	for i in range(16,0,-1):
		draw_circle(Vector2.ZERO,size.y*(.20+i*.006),Color(glow,intensity*.013))
	draw_set_transform(Vector2.ZERO)
	if reaction>0 and not reduced_motion:
		for j in range(5):
			var angle := j*TAU/5+clock
			var center := Vector2(size.x*.5,size.y*.45)+Vector2(cos(angle)*size.x*.6,sin(angle)*size.y*.4)
			preload("res://core/quest/art.gd").star(self,center,5+reaction*2,Color(glow,.85))
		for direction in [-1,1]:
			var origin := Vector2(size.x*.5+direction*size.x*.46,size.y*.23)
			var bolt := PackedVector2Array([origin,origin+Vector2(-direction*9,15),origin+Vector2(direction*5,13),origin+Vector2(-direction*6,29)])
			draw_polyline(bolt,Color(glow,.85),3,true)
	var bob := sin(clock*2.5)*1.5
	if animation=="move": bob = -absf(sin(clock*9))*4
	if animation=="success": bob = -absf(sin(clock*5))*14
	if reduced_motion: bob = 0
	var lean := -.08 if animation=="think" else sin(clock*4)*.025
	if reduced_motion: lean = 0
	var base := Vector2(size.x/2,size.y*.72+bob)
	var tint := Color.WHITE.lerp(glow,minf(.18,reaction*.12)) if not reduced_motion else Color.WHITE
	if is_instance_valid(pet):
		pet.visible = person=="katze"
		if pet.visible:
			if pet_size!=size: build_pet_mesh()
			pet.position = Vector2(size.x/2,size.y/2+bob)
			pet.rotation = lean
			pet.scale = Vector2(facing,1)
			pet.modulate = tint
			pet.material.set_shader_parameter("phase",clock)
			pet.material.set_shader_parameter("walking",animation=="move" and not reduced_motion)
			pet.material.set_shader_parameter("still",reduced_motion)
			pet.material.set_shader_parameter("sprite_size",size)
			return
	draw_set_transform(base,lean,Vector2(facing,1))
	var swing := sin(clock*9)*.22 if animation=="move" and not reduced_motion else 0.0
	for leg in range(2):
		var hip := Vector2((-1 if leg==0 else 1)*scale_size.x*.13,0)
		draw_set_transform(base+Vector2(hip.x*facing,0),lean+swing*(1 if leg==0 else -1),Vector2(facing,1))
		var destination := Rect2(Vector2(-scale_size.x*.5-hip.x if leg==0 else -hip.x,0),Vector2(scale_size.x*.5,scale_size.y*.28))
		draw_texture_rect_region(texture,destination,Rect2(Vector2(leg*w*.5,h*.72),Vector2(w*.5,h*.28)),tint)
	draw_set_transform(base,lean,Vector2(facing,1))
	draw_texture_rect_region(texture,Rect2(Vector2(-scale_size.x*.5,-scale_size.y*.72),Vector2(scale_size.x,scale_size.y*.72)),Rect2(Vector2.ZERO,Vector2(w,h*.72)),tint)
	draw_set_transform(Vector2.ZERO)

func build_pet_mesh() -> void:
	# A continuous mesh keeps fur intact while four paws and the tail move.
	# The cat never uses the two-legged human sprite cut.
	pet_size = size
	var vertices := PackedVector3Array()
	var uvs := PackedVector2Array()
	var indices := PackedInt32Array()
	const COLS := 20
	const ROWS := 28
	for y in range(ROWS+1):
		for x in range(COLS+1):
			var uv := Vector2(float(x)/COLS,float(y)/ROWS)
			uvs.append(uv)
			var at := (uv-Vector2.ONE*.5)*size
			vertices.append(Vector3(at.x,at.y,0))
	for y in range(ROWS):
		for x in range(COLS):
			var i := y*(COLS+1)+x
			indices.append_array(PackedInt32Array([i,i+1,i+COLS+1,i+1,i+COLS+2,i+COLS+1]))
	var arrays := []
	arrays.resize(Mesh.ARRAY_MAX)
	arrays[Mesh.ARRAY_VERTEX] = vertices
	arrays[Mesh.ARRAY_TEX_UV] = uvs
	arrays[Mesh.ARRAY_INDEX] = indices
	var mesh := ArrayMesh.new()
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
	pet.mesh = mesh
