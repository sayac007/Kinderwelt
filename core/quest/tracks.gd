extends RefCounted
const ITEMS := {
 "funkenflug":{"title":"Funkenflug","path":"res://assets/music/funkenflug.wav","color":"e9bd60","icon":"gear"},
 "stars":{"title":"Sternensprung","path":"res://assets/music/stars.wav","color":"bbb4d6","icon":"moon"},
 "meadow":{"title":"Wiesenwind","path":"res://assets/music/meadow.ogg","color":"b6ce8d","icon":"leaf"},
 "gears":{"title":"Zahnrad-Tanz","path":"res://assets/music/gears.ogg","color":"e8b990","icon":"gear"},
 "bounce":{"title":"Farbensprung","path":"res://assets/music/bounce.ogg","color":"e3a48b","icon":"sun"},
 "stories":{"title":"Wolkenbuch","path":"res://assets/music/stories.ogg","color":"b8bfdc","icon":"moon"},
 "garden":{"title":"Gartensprung","path":"res://assets/music/garden.ogg","color":"bed39a","icon":"leaf"},
 "friends":{"title":"Hand in Hand","path":"res://assets/music/friends.ogg","color":"ddb4ba","icon":"sun"},
 "rain":{"title":"Regentropfen","path":"res://assets/music/rain.ogg","color":"a8cdd8","icon":"drop"},
 "victory":{"title":"Geschafft!","path":"res://assets/music/victory.ogg","color":"ebcd7b","icon":"sun"}}
const WORLDS := {"math":"bounce","german":"stories","logic":"gears","success":"victory"}
static func resolve(world: String) -> String:
 return WORLDS.get(world,world)
