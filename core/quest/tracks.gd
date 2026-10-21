extends RefCounted
const ITEMS := {
 "wiener_blut":{"title":"Wiener Blut","composer":"J. Strauss II","detail":"Walzerauszug","path":"res://assets/music/wiener_blut.ogg","color":"e9bd60","icon":"sun"},
 "babbino":{"title":"O mio babbino caro","composer":"G. Puccini","detail":"Themenauszug","path":"res://assets/music/babbino.ogg","color":"ddb4ba","icon":"leaf"},
 "french_song":{"title":"Altes französisches Lied","composer":"P. I. Tschaikowski","detail":"Klavier","path":"res://assets/music/french_song.ogg","color":"b8bfdc","icon":"moon"},
 "consolation":{"title":"Consolation Nr. 1","composer":"F. Liszt","detail":"Klavier","path":"res://assets/music/consolation.ogg","color":"bed39a","icon":"leaf"}}
const DEFAULT := "wiener_blut"
const WORLDS := {"math":"wiener_blut","german":"babbino","logic":"french_song","success":"consolation"}
static func resolve(world: String) -> String:
	return WORLDS.get(world,world)
static func next(id: String,direction := 1,shuffle := false,repeat := false) -> String:
	var ids := ITEMS.keys()
	if repeat and ITEMS.has(id): return id
	if shuffle and direction>0:
		ids.erase(id)
		return ids.pick_random()
	return ids[posmod(ids.find(id)+direction,ids.size())]
