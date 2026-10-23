extends RefCounted
const LOCALES := ["de","en","ru"]
const NAMES := {"de":"Deutsch","en":"English","ru":"Русский"}
static var catalog := {}
static func locale_name(locale: String,current: String) -> String:
	if current=="ru": return {"de":"Немецкий","en":"Английский","ru":"Русский"}[locale]
	if current=="en": return {"de":"German","en":"English","ru":"Russian"}[locale]
	return NAMES[locale]
static func music(id: String,field: String,locale: String) -> String:
	if locale=="ru": return data().music[id][field]
	return preload("res://core/quest/tracks.gd").ITEMS[id][field]
static func data() -> Dictionary:
	if catalog.is_empty(): catalog=JSON.parse_string(FileAccess.get_file_as_string("res://games/quest/languages.json"))
	return catalog
static func text(key: String,locale := "de") -> String:
	var entries: Dictionary = data().ui
	return entries.get(key,{}).get(locale,key)
static func object_name(id: String,locale := "de") -> String:
	return data().objects.get(id,{}).get(locale,id)
static func task(source: Dictionary,locale := "de") -> Dictionary:
	var result := source.duplicate(true)
	if source.get("variants",{}).has(locale): result.merge(source.variants[locale],true)
	var words: Dictionary = source.get("texts",{}).get(locale,{})
	result.prompt = words.get("prompt",source.prompt)
	result.tip = words.get("tip",source.tip)
	return result
