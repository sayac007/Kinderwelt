extends RefCounted
const ITEMS := {
 "adventure_workshop":{"title":"Funkenflug","path":"res://assets/music/adventure/workshop.wav","color":"e9bd60","icon":"gear"},
 "adventure_stars":{"title":"Sternensprung","path":"res://assets/music/adventure/stars.wav","color":"bbb4d6","icon":"moon"},
 "meadow":{"title":"Wiesenwind","path":"res://assets/music/modern/meadow.ogg","color":"b6ce8d","icon":"leaf"},
 "gears":{"title":"Zahnrad-Tanz","path":"res://assets/music/modern/gears.ogg","color":"e8b990","icon":"gear"},
 "market":{"title":"Markttag","path":"res://assets/music/modern/market.ogg","color":"e3a48b","icon":"sun"},
 "stories":{"title":"Wolkenbuch","path":"res://assets/music/modern/stories.ogg","color":"b8bfdc","icon":"moon"},
 "garden":{"title":"Gartensprung","path":"res://assets/music/modern/garden.ogg","color":"bed39a","icon":"leaf"},
 "together":{"title":"Hand in Hand","path":"res://assets/music/modern/together.ogg","color":"ddb4ba","icon":"sun"},
 "rain":{"title":"Regentropfen","path":"res://assets/music/modern/rain.ogg","color":"a8cdd8","icon":"drop"},
 "victory":{"title":"Geschafft!","path":"res://assets/music/modern/victory.ogg","color":"ebcd7b","icon":"sun"}}
const WORLDS := {"map":"meadow","logic":"gears","math":"market","language":"stories","autonomy":"garden","social":"together","success":"victory"}
static func resolve(world: String) -> String:
	return WORLDS.get(world,world)
