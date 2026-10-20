extends RefCounted
# New module text is keyed centrally. Missing translations fall back to German.
static var locale := "de"
static var german: Dictionary = {}
static var translated: Dictionary = {}

static func load_table(path: String) -> Dictionary:
	if not FileAccess.file_exists(path): return {}
	var parser := JSON.new()
	if parser.parse(FileAccess.get_file_as_string(path)) != OK: return {}
	return parser.data if parser.data is Dictionary else {}

static func set_locale(language: String) -> void:
	locale = language
	german = load_table("res://content/locales/de.json")
	translated = load_table("res://content/locales/" + language + ".json") if language in ["de", "en"] else {}

static func has_key(key: String) -> bool:
	if german.is_empty(): set_locale(locale)
	return german.get(key) is String and not german[key].is_empty()

static func message(key: String) -> String:
	if german.is_empty(): set_locale(locale)
	return str(translated.get(key, german.get(key, key)))
